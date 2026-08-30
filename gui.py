#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" gui.py 
Tkinter User Interface zur Konfiguration
"""

# from collections.abc import Callable
import tkinter as tk
from tkinter import ttk

# from tkinter.messagebox import askretrycancel
from tkinter.messagebox import showinfo

# from typing import Callable, Literal
import webbrowser
import socket

# http://stackoverflow.com/questions/166506/
# finding-local-ip-addresses-using-pythons-stdlib
def get_ip_address():
    try:
        return ([(s.connect(('8.8.8.8', 80)),s.getsockname()[0], s.close())
           for s in [socket.socket (socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
    except:
        return "localhost"

# class Gui: ------------------------------------------------------------------------
class Gui:
    def __init__(self):
        self.root = tk.Tk()

        # Main-Window:        
        self.root.title ("Midi 2 OSC")
        self.root.geometry("640x400+30+30")
        self.root.columnconfigure (0, weight=1)
        self.root.rowconfigure (0, weight=1)
        self._job = None # siehe self.keep_connected() und self.disconnect()

        # Keyboard bindings:
        self.root.bind("<Control-w>", self.quit)
        self.root.bind ("q", self.quit)

        self.style = ttk.Style ()
        self.style.theme_use ("alt")

        self.create_widgets ()
        self.root.option_add('*tearOff', tk.FALSE)
        self.menu = MainMenu (self)


    def create_widgets (self):
        """ widgets for gui

        Basis-Frame: self.content
        alle weiteren Frames werden in self.content platziert.
        """

        self.content = ttk.Frame(self.root)
        self.content.grid(row=0, column=0, sticky="N, W, E, S")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        self.oscinfo = OscFrame (self.content)
        self.oscinfo.frame.grid (row=1, column=0, padx=5, pady=5, sticky="W")

        self.midiinfo = MidiFrame (self.content)
        self.midiinfo.frame.grid (row=2, column=0, padx=5, pady=5, sticky="W")

        # Message-Box
        self.msgcontent = tk.StringVar()
        self.msgframe = ttk.Frame (self.content, borderwidth=5)
        self.msgframe["height"] = 30
        self.msglab = ttk.Label (self.msgframe, textvariable=self.msgcontent)
        self.msgframe.grid (row=4, column=0, columnspan=2, 
                            sticky="W,E", padx=5, pady=10) 
        self.msglab.grid (row=0, column=0, sticky="W,E") 


    def port_changed (self, *args):
        """ evaluate changes in osc_port Entry """
        print ("port changed")


    def message (self, txt):
        """Ausgabe von Meldungen, Infos    
        """
        self.msgcontent.set (txt)

    def quit (self, event=None):
        """ disconnect and close app """
        print ("disconnect and quit...")
        self.root.destroy ()


# class MidiFrame: ------------------------------------------------------------------------
class MidiFrame (ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.container = parent
        self.frame = ttk.Frame(self.container, borderwidth=5, relief="sunken")
        self.frame.columnconfigure (0, weight=1)
        self.frame.columnconfigure (1, weight=2)
        self.frame.columnconfigure (2, weight=4)

        # midi-input:
        # Label:
        self.midi_descriptor = ttk.Label (self.frame, text="MIDI-Input:")
        self.midi_descriptor.grid (row=0, column=0, sticky="W", padx=10)

        # Auswahl:
        self.midiinput_selector  = tk.StringVar()
        self.selectedmidi = ttk.Combobox(self.frame, textvariable=self.midiinput_selector)
        self.selectedmidi.grid (row=0, column=1, sticky="W")

        # Fillspace:
        self.fillspace1 = ttk.Frame (self.frame)
        self.fillspace1.grid (row=0, column=2, sticky="W")
        
        # converter-input:
        # Label:
        self.converter_descriptor = ttk.Label (self.frame, text="Converter:")
        self.converter_descriptor.grid (row=1, column=0, sticky="W", padx=10)

        # Auswahl:
        self.converter_selector  = tk.StringVar()
        self.selectedconverter = ttk.Combobox(self.frame, textvariable=self.converter_selector)
        self.selectedconverter.grid (row=1, column=1, sticky="W")

        # Fillspace:
        self.fillspace2 = ttk.Frame (self.frame)
        self.fillspace2.grid (row=1, column=2, sticky="W")
        
        # midi Monitor:
        self.midimonitor = tk.Text (self.frame, height=10)
        self.midimonitor.insert ("1.0", "midi Monitor")
        self.midimonitor.grid (row=2, column=0, columnspan=3, sticky="EW")

        
# class OscFrame: ------------------------------------------------------------------------
class OscFrame (ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.container = parent
        self.frame = ttk.Frame(self.container, borderwidth=5, relief="sunken")
        self.outip = tk.StringVar()
        self.outport = tk.StringVar()
        # self.msg_function = print

        # Einlesen von ip und port - Defaultwerte:
        self.get_config()
        
        # Eingabe ip und port:
        self.header = ttk.Label (self.frame, text="Verbindung mit Chamsys:")
        self.header.grid (row=0, column=0, columnspan=2,
                          sticky='W')
        
        self.lb1 = ttk.Label (self.frame, text="Diese IP")
        self.lb1.grid (row=1, column=0,
                       sticky='W', padx=10)

        self.showip = ttk.Label (self.frame, text=get_ip_address())
        self.showip.grid (row=1, column=1,
                       sticky='W', padx=2)
    
        self.lb2 = ttk.Label (self.frame, text="Chamsys IP")
        self.lb2.grid (row=2, column=0,
                       sticky='W', padx=10)
    
        self.ipentry = ttk.Entry (self.frame, textvariable = self.outip)
        self.ipentry.grid (row=2, column=1)
        
        self.lb4 = ttk.Label (self.frame, text="Chamsys Port")
        self.lb4.grid (row=4, column=0,
                       sticky='W', padx=10)
        
        self.portentry = ttk.Entry (self.frame, width=6,
                                       textvariable = self.outport)
        self.portentry.grid (row=4, column=1, sticky='W')

        
    def get_config(self):
        """ Config-Daten einlesen """
        self.outip.set ("127.0.0.1")
        self.outport.set ("8000")

        
# class MainMenu: ------------------------------------------------------------------------
class MainMenu:
    """ Menüstruktur des Hauptfensters """
    
    def __init__(self, gui):
        self.root = gui.root
        self.menu = tk.Menu (self.root)
        self.root.config(menu=self.menu)
        
        self.connectmenu = tk.Menu(self.menu)
        self.menu.add_cascade (label = "Verbindung", menu = self.connectmenu)
        self.connectmenu.add_command (label = "Exit", command=gui.quit)

        self.helpmenu = tk.Menu (self.menu)
        self.menu.add_cascade (label="Hilfe", menu=self.helpmenu)
        self.helpmenu.add_command (label="Über",
                                   command=self.about)
        self.helpmenu.add_command (label="Nach Updates suchen",
                                   command = self.update)

    def about(self):
        showinfo (message= \
"""
Midi 2 OSC

(c) Gunther Seiser 2026
"""
        )

    def update(self):
        url = "https://drive.google.com/folderview?id=0B6Yq29kAcfcVfkZ4MVFDRUxmMWdvMV9aNDdEOG1oUmtZSUtsakdBcXpFbjJJQjlZY29jdkk&usp=sharing"
        webbrowser.open_new_tab(url)

# ------------------------------------------------------------------
if __name__ == "__main__":
    app = Gui()

    def testmessage (txt:str):
        """ test message line"""
        app.message (txt)

    app.root.bind ("m", lambda e: testmessage ("this is a test message"))
    
    try:
        app.root.protocol("WM_DELETE_WINDOW", app.quit) # close-Button        
        app.root.mainloop()
    except:
        app.quit ()


        
