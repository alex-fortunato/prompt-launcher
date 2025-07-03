#!/bin/bash
  pyinstaller \
  --name pl-chat \
  --windowed \
  --onedir \
  --add-data "../src/icons:icons" \
  --distpath ../dist \
  --workpath ../build \
  --specpath ../spec \
  pl-chat.py


