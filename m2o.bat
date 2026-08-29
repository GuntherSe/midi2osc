@echo off
echo Starte midi2osc ...

call .venv\Scripts\activate
py midi2osc.py

deactivate

