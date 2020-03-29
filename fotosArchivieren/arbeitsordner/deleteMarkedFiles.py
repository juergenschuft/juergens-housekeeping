#!/usr/bin/python

import os
import glob, os

# ln -sfn /a/new/path curWorkDir

srcDir = "curWorkDir"

print("Auf geht's! srcDir: " + srcDir)

# cd into scripts directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# deleteFolderIfExists(skpDir)

# db = TinyDB("picimport.log.json")

# get list of all source files
fileList = glob.glob(srcDir + "/*.toBeDeleted.*")

print(str(len(fileList)) + " Dateien im Quell-Verzeichnis >" + srcDir + "< gefunden")

for f in fileList:
    os.remove(f)
    print("die Datei " + f + " wurde erfolgreich geloescht")
