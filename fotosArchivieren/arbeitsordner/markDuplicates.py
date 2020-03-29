#!/usr/bin/python

import os
# import sys
# import shutil

# from datetime import datetime
# from PIL import Image
# from PIL import ExifTags
# from tinydb import TinyDB, Query
#import time

# quelle: https://stackoverflow.com/questions/20252669/get-files-from-directory-argument-sorting-by-size
def get_files_by_file_size(dirname, reverse=False):
    """ Return list of file paths in directory sorted by file size """

    # Get list of files
    filepaths = []
    for basename in os.listdir(dirname):
        filename = os.path.join(dirname, basename)
        if os.path.isfile(filename):
            filepaths.append(filename)

    # Re-populate list with filename, size tuples
    for i in range(len(filepaths)):
        filepaths[i] = (filepaths[i], os.path.getsize(filepaths[i]))

    # Sort list by file size
    # If reverse=True sort from largest to smallest
    # If reverse=False sort from smallest to largest
    filepaths.sort(key=lambda filename: (filename[1], filename[0]), reverse=reverse)

    # Re-populate list with just filenames
    # for i in range(len(filepaths)):
    #    filepaths[i] = filepaths[i][0]

    return filepaths

# ln -sfn /a/new/path curWorkDir

srcDir = curWorkDir

print("Auf geht's! srcDir: " + srcDir)

# cd into scripts directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# deleteFolderIfExists(skpDir)

# db = TinyDB("picimport.log.json")

# get list of all source files
fileList = get_files_by_file_size(srcDir)

print(str(len(fileList)) + " Dateien im Quell-Verzeichnis >" + srcDir + "< gefunden")

lastFileName = ""
lastFileSize = 0

for f in fileList:
    curFileName = f[0]
    curFileSize = f[1]
    if curFileSize != lastFileSize:
        lastFileName = curFileName
        lastFileSize = curFileSize
        continue
    # print("die Dateien " + lastFileName + " und " + curFileName + " haben die gleiche Groesse.")
    if "." in curFileName:
        nameParts = curFileName.split(".")
        fileExt = "." + nameParts[-1]
        fileMain = nameParts[0]
    else:
        fileExt = ""
        fileMain = curFileName
    fileNew = fileMain + ".toBeDeleted" + fileExt
    # print("die Datei " + curFileName + " wird umbenannt in  " + fileNew)
    if os.path.exists(fileNew):
        print("Die Datei " + fileNew + " existiert bereits, deshalb wird " + curFileName + " nicht umbenannt.")
        continue
    os.rename(curFileName, fileNew)
    lastFileName = curFileName
    lastFileSize = curFileSize
