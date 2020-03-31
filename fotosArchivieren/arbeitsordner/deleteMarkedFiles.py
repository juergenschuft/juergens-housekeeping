#!/usr/bin/python

import os
import glob, os

# ln -sfn '/media/shuttle/DatenGesichert/private_pictures/Fotos 2013/02 Februar' curWorkDir

srcDir = "curWorkDir"

print("Auf geht's! srcDir: " + srcDir)

# cd into scripts directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

for dirpath, dirnames, filenames in os.walk(srcDir):
    for filename in [f for f in filenames if f.endswith(".toBeDeleted")]:
        f = os.path.join(dirpath, filename)
        os.remove(f)
        print("die Datei " + f + " wurde erfolgreich geloescht")
