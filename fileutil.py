#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path

# https://stackoverflow.com/questions/33135038/how-do-i-use-os-scandir-to-return-direntry-objects-recursively-on-a-directory


def get_curdir (spath:str='.', basedir:str='') ->str:
    """ aus spath (=searchpath) absolut-Pfad erzeugen 
    
    spath = Suchpfad
    basedir = Pfad vor Suchpfad
    z.B.: c:\\data\\basedir\\spath oder spath oder ..
    """
    if basedir:
        if os.path.isabs (basedir):
            cwd = basedir
        else:
            cwd = os.path.abspath (basedir)
    else:
        cwd = os.getcwd()

    if os.path.isabs(spath): # abs. Pfad
        if os.path.isdir (spath):
            return spath
        return cwd

    if spath == '.':
        ret = cwd
    elif spath == '..':
        ret = os.path.dirname (cwd)
    else:
        ret = os.path.join (cwd, spath)

    if (os.path.isdir (ret)):
        return ret
    else:
        return cwd


def list_files (ftype:str="" ) ->list:
    """ list directory 'path' mit Dateityp 'ftype'
spath: z.B. '.', 'subdir', ...
ftype: Dateiendung, Groß-/Kleinschreibung egal, '.xyz' oder 'xyz'
return: Dict mit allen Subdirs in Liste, dann alle Dateien in Liste
"""
    filelist = []

    if ftype:
        ftypelow = ftype.lower()
    else:
        ftypelow = ""

    searchdir =  os.getcwd()   
    for entry in os.scandir (searchdir):
        if entry.is_dir (follow_symlinks=False):
            pass
        elif ftype == "":
            filelist.append (entry.name)
        elif entry.name.lower().endswith(ftypelow):
                                    # Groß- und Kleinschreibung egal
            filelist.append (entry.name)
    ret = sorted (filelist, key=str.lower)
    
    return ret

# ----------------------------------------------------------------

if __name__ == "__main__":

    print (f"all files: {list_files ()}")
    print (f"python files: {list_files ('py')}")
    print (f"csv files: {list_files ('csv')}")
    