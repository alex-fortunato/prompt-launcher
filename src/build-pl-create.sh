#!/bin/bash
  pyinstaller \
  --name pl-music \
  --windowed \
  --onedir \
  --add-data "../src/icons:icons" \
  --distpath ../dist \
  --workpath ../build \
  --specpath ../spec \
  pl-music.py


