#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" main.py

Start this module!
"""

import mido
import sys
import shelve
# import queue
import threading
from pythonosc import udp_client
from gui import Gui
from converter import Converter
from fileutil import list_files

# -----------------------------------------------------------------------------
# class Config:
class Config:
    def __init__(self):
        self.conffile = sys.argv[0][:-3]
        self.midi_inputs = []
        self.converters = []
        self.get_midi_inputs ()
        self.converters = list_files ("csv")
        self.get_config ()


    def get_midi_inputs (self):
        """ Midi Geräte einlesen """
        self.midi_inputs = mido.get_input_names() # type: ignore


    def get_config (self): 
        """ read config from conffile 
        
        provide default value if key not found
        """
        with shelve.open (self.conffile) as cfg:
            if "osc_ip" in cfg:
                self.osc_ip = cfg["osc_ip"]
            else:
                self.osc_ip = "127.0.0.1"

            if "osc_port" in cfg:
                self.osc_port = cfg["osc_port"]
            else:
                self.osc_port = "8000"

            if "midi_device" in cfg:
                self.midi_device = cfg["midi_device"]
                if not self.midi_device in self.midi_inputs:
                    self.midi_device = ""
            else:
                self.midi_device = ""

            if "converter" in cfg:
                self.converter = cfg["converter"]
                if not self.converter in self.converters:
                    self.converter = ""
            else:
                self.converter = ""


    def save_config (self):
        """ write config data to conffile """
        with shelve.open (self.conffile) as cfg:
            cfg["osc_ip"] = self.osc_ip
            cfg["osc_port"] = self.osc_port
            cfg["midi_device"] = self.midi_device
            cfg["converter"] = self.converter
            cfg.sync ()

# -----------------------------------------------------------------------------
class Midicontroller (threading.Thread):
    """ """
    def __init__(self, device = "") -> None:
        threading.Thread.__init__ (self, target=self.run)
        self.devicename = device
        self.port = None
        self.eval = print

        try:
            self.port = mido.open_input (self.devicename) # type: ignore
        except:
            print ("Midicontroller nicht gefunden.")

        self.daemon = True
        self.start ()


    def set_controller (self, device):
        """ """
        self.devicename = device
        if self.port:
            self.port.close ()

        try:
            self.port = mido.open_input (self.devicename) # type: ignore
        except:
            print ("Midicontroller nicht gefunden.")

    def set_eval_function (self, new_func):
        """ eval-Funktion zuweisen """
        self.eval = new_func

    def eval_msg (self, msg):
        """ midi message auswerten 

        msg: mido Message
        eval: print oder andere eval-Funktion
        """
        self.eval (msg)

    def run (self):
        """ thread starten """
        while True:
            if self.port is not None:
                for msg in self.port.iter_pending ():
                    self.eval_msg (msg)

    

# --- main --------------------------------------------------------------------

cfg = Config() # instance of Config
gui = Gui ()   # instance of Gui
mc  = Midicontroller (cfg.midi_device)
cv  = Converter (cfg.converter)
# print (f"CSV: {cv.data()}")

# OSC client:
osc = udp_client.SimpleUDPClient(cfg.osc_ip, int(cfg.osc_port))


# Midi device:
def midiinput_changed (*args):
    cfg.midi_device = gui.midiinfo.midiinput_selector.get ()
    gui.message (f"midi input changed: {cfg.midi_device}")
    mc.set_controller (cfg.midi_device)

gui.midiinfo.selectedmidi["values"] = cfg.midi_inputs
gui.midiinfo.selectedmidi.bind ("<<ComboboxSelected>>", midiinput_changed)
gui.midiinfo.midiinput_selector.set (cfg.midi_device)

def eval_midi (args):
    """ Midi Auswerte-Funktion """
    gui.midiinfo.midimonitor.insert ("1.0", "\n")
    gui.midiinfo.midimonitor.insert ("1.0", args)
    control = args.control
    value   = args.value
    # print (f"Message:{control}, {value}")
    if control in cv.controllers:
        gui.message (f"{cv.converter(control)}, {float (int(value) / 127)}")
        osc.send_message (cv.converter(control), float (int(value) / 127))

mc.set_eval_function (eval_midi)

# converter:
def converter_changed (*args):
    cfg.converter = gui.midiinfo.converter_selector.get()
    gui.message (f"converter changed: {cfg.converter}")
    cv.name (cfg.converter)

gui.midiinfo.selectedconverter["values"] = cfg.converters
gui.midiinfo.selectedconverter.bind ("<<ComboboxSelected>>", converter_changed)
gui.midiinfo.converter_selector.set (cfg.converter)

# OSC device:
gui.oscinfo.ipentry.delete (0, "end")
gui.oscinfo.ipentry.insert (0, cfg.osc_ip)
gui.oscinfo.portentry.delete (0, "end")
gui.oscinfo.portentry.insert (0, cfg.osc_port)

oscclient = udp_client.SimpleUDPClient(cfg.osc_ip, int(cfg.osc_port))

# Auswerten von Eingaben in der Gui
def port_changed (*args):
    cfg.osc_port = gui.oscinfo.portentry.get ()
    gui.message (f"osc port changed: {cfg.osc_port}")

def ip_changed (*args ):
    cfg.osc_ip = gui.oscinfo.ipentry.get ()
    gui.message (f"osc io changed: {cfg.osc_ip}")

gui.oscinfo.outport.trace_add ("write", port_changed)
gui.oscinfo.outip.trace_add ("write", ip_changed)

# Menüeintrag zum Speichern der config:
gui.menu.connectmenu.add_command (label = "Config speichern", 
                                  command=cfg.save_config)

# mainloop:
try:
    gui.root.protocol("WM_DELETE_WINDOW", gui.quit) # close-Button        
    gui.root.mainloop()
except:
    print ("Es ist ein Fehler bei mainloop aufgetreten.")
    gui.quit ()

