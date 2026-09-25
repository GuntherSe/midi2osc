# MIDI 2 OSC

This program is intended to support a lightdesk like Chamsys consoles with an additional MIDI controller. It receives MIDI controls and sends corresponding OSC strings to the light desk to trigger or fade any button or fader that can be reached by OSC. Typically these are Playback faders or Executer elements.

## Features

* Graphical User interface
* converter data are stored in CSV format. Therefore it can be edited with any text editor 
* suitable for any MIDI device that sends control change data

## Installation

Python best practice is to create a project-specific `virtual environment`, for example in the current working directory. 
For the start scripts create a virtual environment called *.venv*.
Switch to the working directory where you cloned the repository.

### Windows: 

    py -m venv .venv
    .venv\Scripts\activate
    py -m pip install -r requirements.txt

### Linux

You have to install Tkinter:

    sudo apt update
    sudo apt install python3-tk

Now, install the Python-specific modules:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

## Run

In a Windows terminal run  `m2o.bat`, in a Linux terminal run `m2o.sh`. 



## License

[MIT](LICENSE.md)