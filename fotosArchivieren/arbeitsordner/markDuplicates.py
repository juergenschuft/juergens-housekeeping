#!/usr/bin/python

import os

# ln -sfn /a/new/path curWorkDir

srcDir = "curWorkDir"
# srcDir = "10 Oktober"

### definitionen

# quelle: https://stackoverflow.com/questions/20252669/get-files-from-directory-argument-sorting-by-size
def get_files_by_file_size(dirname, reverse=False):
    """ Return list of file paths in directory sorted by file size """

    # Get list of files
    filepaths = []
    for basename in os.listdir(dirname):
        filename = os.path.join(dirname, basename)
        if os.path.isfile(filename):
            filepaths.append((filename, basename))

    # Re-populate list with filename, size tuples
    for i in range(len(filepaths)):
        filepaths[i] = (filepaths[i][0], os.path.getsize(filepaths[i][0]), filepaths[i][1])

    # Sort list by file size
    # If reverse=True sort from largest to smallest
    # If reverse=False sort from smallest to largest
    filepaths.sort(key=lambda filename: (filename[1], filename[0]), reverse=reverse)

    # Re-populate list with just filenames
    # for i in range(len(filepaths)):
    #    filepaths[i] = filepaths[i][0]

    return filepaths

def processDir(srcDir):
    
    # get list of all source files
    fileList = get_files_by_file_size(srcDir)
    
    nrOfFiles = len(fileList)
    
    # print(str(nrOfFiles) + " Dateien im Quell-Verzeichnis >" + srcDir + "< gefunden")
    
    if nrOfFiles < 1:
        return nrOfFiles
    
    lastDir = ""
    lastFileName = ""
    lastFileSize = 0
    lastFileDay = "" # 2013_01_12
    
    for f in fileList:
        curFileName = f[2]
        curFileSize = f[1]
        curFileDay = curFileName[ 0 : 10]
        print("curFileName: " + curFileName + " curFileSize: " + str(curFileSize))
    #    continue
        if (curFileSize != lastFileSize or curFileDay != lastFileDay):
    #        print("die Dateien " + lastFileName + " und " + curFileName + " sind ungleich.")
            lastFileName = curFileName
            lastFileSize = curFileSize
            lastFileDay  = curFileDay
            continue
    #    print("die Dateien " + lastFileName + " und " + curFileName + " sind gleich.")
        if "." in curFileName:
            nameParts = curFileName.split(".")
            fileExt = "." + nameParts[-1]
            fileMain = nameParts[0]
        else:
            fileExt = ""
            fileMain = curFileName
        fileNew = os.path.join(srcDir, fileMain + ".toBeDeleted" + fileExt)
        fileOld = os.path.join(srcDir, curFileName)

        print("die Datei " + fileOld + " wird umbenannt in  " + fileNew)
        if os.path.exists(fileNew):
            print("Die Datei " + fileNew + " existiert bereits, deshalb wird " + fileOld + " nicht umbenannt.")
            continue
        os.rename(fileOld, fileNew)
        lastFileName = curFileName
        lastFileSize = curFileSize
        lastFileDay  = curFileDay

    return nrOfFiles

### hauptprogramm

print("Auf geht's! srcDir: " + srcDir)

# cd into scripts directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
# os.chdir(srcDir)

for root, dirs, files in os.walk(srcDir):
    # print("dirs: " + str(len(dirs)))
    for d in dirs:
        curDir = os.path.relpath(os.path.join(root, d), dname)
        # print("gleich: " + curDir)
        processDir(curDir)
        
print("fertig")
