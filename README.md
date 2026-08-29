# MIDI 2 OSC

This program is intended to support a lightdesk like Chamsys consoles with an additional MIDI controller. It receives MIDI controls and sends corresponding OSC strings to the light desk to trigger or fade any button or fader that can be reached by OSC. Typically these are Playback faders or Executer elements.

## Features

* Graphical User interface
* converter data are stored in CSV format. Therefore it can be edited with any text editor 
* suitable for any MIDI device that sends control change data

## Installation

Python best practice is to create a project-specific `virtual environment`, for example in the current working directory. 
T create a virtual environment called *.venv* in Windows, run the command:

    py -m venv .venv

To activate this environment, run:

    .venv\Scripts\activate

Then, install the requred packages, listed in requirements.txt:

    py -m pip install -r requirements.txt

## Run

In a terminal, run:

    m2o.bat



## License

[MIT](LICENSE.md)