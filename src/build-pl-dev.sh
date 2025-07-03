#!/bin/bash
  pyinstaller \
  --name pl-dev \
  --windowed \
  --onedir \
  --add-data "../src/icons:icons" \
  --distpath ../dist \
  --workpath ../build \
  --specpath ../spec \
  pl-dev.py


