#!/Users/alexanderfortunato/Development/prompt-launcher/.venv/bin/python3.13
import os
import sys
from pathlib import Path

from PIL import Image, ImageQt
from PySide6 import QtCore, QtGui, QtWidgets

# --- Configuration -------------------------------------------------------

ICON_NAMES = {
    'm': 'Messages',
    'w': 'WhatsApp',
    'd': 'Discord',
    'g': 'Gmail',
}

# Commands to run for each key
LAUNCH_CMDS = {
    'm': ['open', '-a', 'Messages'],
    'w': ['open', '-a', 'WhatsApp'],
    'd': ['open', '-a', 'Discord'],
    'g': ['open', '-a', 'Firefox', 'https://mail.google.com'],
}

ICON_SIZE = (84, 84)
ICONS_DIR = Path(__file__).parent / 'icons'
MENU_BAR_HEIGHT = 42
FONT_FAMILY = 'JetBrains Mono'
FONT_SIZE = 15  # point size for text labels
UI_HEIGHT_REDUCTION = 100# pixels to reduce overall window height

# --- Main Window ---------------------------------------------------------

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
        # set up horizontal layout for icon containers
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
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
