#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" class Midiconverter

define which midi inputs you want to listen to
define which osc command you want to send 

- read converter info from CSV file:
  
"""
import os
import os.path
import mido
import csv

class Converter ():
    """ open and read csv file """

    def __init__(self, newname=None):

        self.filename = newname
        self.csvdata = {}
        self.controllers = []

        # fieldnames:
        if not self.filename:
            self._fieldnames = []

        elif not os.path.isfile (self.filename):
            # print ("File nicht gefunden: ", fname)
            self._fieldnames = []
        else:
            with open (self.filename, 'r',encoding='utf-8',newline='') as pf:
                reader = csv.DictReader (pf, restval= '')
                self._fieldnames = reader.fieldnames
                # file einlesen:
                for row in reader:
                    try:
                        self.csvdata[int(row["control"])] = row["osc"]
                        self.controllers.append (int (row["control"]))
                    except: # ignore comments etc.
                        pass

    def fieldnames (self) :
        """ fieldnames aus CSV-Datei auslesen """
        return self._fieldnames 

    def name (self, newname = ""):
        """ Filename ändern bzw aktuellen Filenamen retournieren
        """
        if newname:
            self.__init__ (newname)

        if not self.filename:
            return ""
        
        if os.path.isfile (self.filename):
            return self.filename
        else:
            return ""
    
    def data (self):
        """ output data """
        return self.csvdata

    def midicontrollers (self) -> list:
        """ list of all found controllers """
        return self.controllers

    def converter (self, key:int) ->str:
        """ if key found in controllers, output corresponding osc string """
        if key in self.controllers:
            return self.csvdata[key]
        else:
            return ""


# ------------------------------------------------------------------
if __name__ == "__main__":
    c = Converter ("nanokontrol2.csv")
    print (f"Fieldnames: {c.fieldnames()}")
    print (c.data())
    print (f"found controls: {c.midicontrollers()}")

    print (f"converter(0) = {c.converter(0)}")
    print (f"converter(10) = {c.converter(10)}")
        