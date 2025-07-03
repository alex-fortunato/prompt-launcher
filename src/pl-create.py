import os
import sys
from pathlib import Path

from PIL import Image, ImageQt
from PySide6 import QtCore, QtGui, QtWidgets

# -- Configuration

ICON_NAMES = {
        'c': 'Cubase',
        'a': 'Ableton',
        'l': 'Logic',
        'p': 'ProTools',
        's': 'Sibelius',
        'o': 'Omnibus',
        'd': 'DaVinciResolve'
}

# Commands to run for each key
LAUNCH_CMDS = {
        'c': ['open', '-a', 'Cubase 14'],
        'a': ['open', '-a', 'Ableton Live 12 Suite'],
        'l': ['open', '-a', 'Logic Pro'],
        'p': ['open', '-a', 'Pro Tools'],
        's': ['open', '-a', 'Sibelius'],
        'o': ['open', '-a', 'Omnibus'],
        'd': ['open', '-a', 'DaVinci Resolve'],
}

ICON_SIZE = (84, 84)
ICONS_DIR = Path(__file__).parent / 'icons'
MENU_BAR_HEIGHT = 42
FONT_FAMILY = 'Jetbrains Mono'
FONT_SIZE = 15
UI_HEIGHT_REDUCTION = 100

# --- Main Window ---

class LauncherWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(
                None,
                QtCore.Qt.WindowType.FramelessWindowHint
                | QtCore.Qt.WindowType.WindowStaysOnTopHint,
        )

        # allow transparent window background
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        # ensure icon and text labels are transparent
        self.setStyleSheet('QLabel { background: transparent; }')

        # load the background PNG
        self._bg_pix = QtGui.QPixmap((ICONS_DIR / 'Background2.png').as_posix())

        self._load_icons()
        self._build_ui()
        self._position_top_center()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        # draw PNG background scaled to widget size
        painter.drawPixmap(self.rect(), self._bg_pix)
        # paint child widgets over the background
        super().paintEvent(event)

    def _load_icons(self):
        self.icons = {}
        for key, name in ICON_NAMES.items():
            img_path = ICONS_DIR / f'{name}.png'
            img = Image.open(img_path).resize(ICON_SIZE, Image.Resampling.LANCZOS)
            qim = ImageQt.ImageQt(img)
            pix = QtGui.QPixmap.fromImage(qim)
            self.icons[key] = pix

    def _build_ui(self):
        # set up horizonatal layout for icon containers
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4) # Left, top, right, bottom
        layout.setSpacing(2)

        # prepare font with desired point size
        font = QtGui.QFont(FONT_FAMILY, FONT_SIZE)

        for key in ICON_NAMES:
            container = QtWidgets.QWidget()
            vbox = QtWidgets.QVBoxLayout(container)

            icon_lbl = QtWidgets.QLabel()
            icon_lbl.setPixmap(self.icons[key])
            icon_lbl.setAlignment(QtCore.Qt.AlignCenter)
            icon_lbl.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)

            text_lbl = QtWidgets.QLabel(key.upper(), alignment=QtCore.Qt.AlignCenter)
            text_lbl.setFont(font)

            vbox.addWidget(icon_lbl)
            vbox.addWidget(text_lbl)
            layout.addWidget(container)

        # make the widget focusable for key events
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            QtWidgets.QApplication.quit()
            return
        ch = event.text().lower()
        if ch in LAUNCH_CMDS:
            self._launch_and_quit(ch)
        else:
            super().keyPressEvent(event)

    def _launch_and_quit(self, key):
        cmd = LAUNCH_CMDS[key]
        QtWidgets.QApplication.quit()
        os.execvp(cmd[0], cmd)

    def _position_top_center(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        # calculate ideal size then reduce height
        self.adjustSize()
        width = self.width()
        height = max(0, self.height() - UI_HEIGHT_REDUCTION)
        self.resize(width, height)
        # center horizontally, offset vertically by menu bar height
        x = (screen.width() - width) // 2
        y = MENU_BAR_HEIGHT
        self.move(x, y)

# --- Entry Point ---------------------------------------------------------

def main():
    app = QtWidgets.QApplication(sys.argv)
    # set the application font and size
    app.setFont(QtGui.QFont(FONT_FAMILY, FONT_SIZE))
    w = LauncherWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()