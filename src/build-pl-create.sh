#!/bin/bash
  pyinstaller \
  --name pl-create \
  --windowed \
  --onedir \
  --add-data "../src/icons:icons" \
  --distpath ../dist \
  --workpath ../build \
  --specpath ../spec \
  pl-create.py


