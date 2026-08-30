#!/bin/bash
# Startscript fot midi2osc

echo "Starte midi 2 osc..."


if [ -d "$HOME/Dokumente" ]; then
  cd $HOME/Dokumente/python/midi2osc
else
  cd $HOME/Documents/python/midi2osc
fi

source .venv/bin/activate
python midi2osc.py

deactivate

