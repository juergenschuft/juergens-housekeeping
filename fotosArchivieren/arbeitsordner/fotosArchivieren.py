#!/usr/bin/python

import os
import sys
import shutil

from datetime import datetime
from PIL import Image
from PIL import ExifTags
from tinydb import TinyDB, Query
#import time

def getExifData(srcDir, fn):
    exifData = {}
    img = Image.open(srcDir + '/' + fn)
    exifDataRaw = img._getexif()
    for tag, value in exifDataRaw.items():
        decodedTag = ExifTags.TAGS.get(tag, tag)
        exifData[decodedTag] = value
    return exifData

def extractFileDateFromName(fn):
    # tries to parse fileName fn to dateTime
    datePatterns=["video-%Y-%m-%d-%H-%M-%S", "%Y%m%d_%H%M%S"]
    patternLenths=[23, 15] # cut away additional chars
    counter = 0
    for curPattern in datePatterns:
        try:
            patternLength = patternLenths[counter]
            counter += 1
            fileDate = datetime.strptime(fn[:patternLength], curPattern)
        except ValueError as ve:
            print('ValueError Raised:', ve)
            continue
        if fileDate!=None:break#got valid time
    return fileDate

def extractImageDate(srcDir, fn):
    "Returns the date and time from image(if available)\nfrom Orthallelous"
    TTags=[('DateTimeOriginal','SubsecTimeOriginal'),#when img taken
    ('DateTimeDigitized','SubsecTimeDigitized'),#when img stored digitally
    ('DateTime','SubsecTime')]#when img file was changed
    #for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
    try:
        exif=getExifData(srcDir, fn)
    except OSError as ose:
        print('OSError Raised:', ose)
        return None
    except AttributeError as ae:
        print('AttributeError Raised:', ae)
        return None
    except IOError as ioe:
        print('IOError Raised:', ioe)
        return None
    
    for i in TTags:
        dT, sub = exif.get(i[0]), exif.get(i[1],0)
        dT = dT[0] if type(dT) == tuple else dT#PILLOW 3.0 returns tuples now
        sub = sub[0] if type(sub) == tuple else sub
        if dT!=None:break#got valid time
    if dT==None:return#found no time tags
 
    T=datetime.strptime('{}.{}'.format(dT,sub),'%Y:%m:%d %H:%M:%S.%f')
    #T=time.mktime(time.strptime(dT, '%Y:%m:%d %H:%M:%S')) + float('0.%s'%sub)
    return T

def extractFileDate(srcDir, fn, nameMainPart):
    fileDate = extractImageDate(srcDir, fn)
    if fileDate!=None:return fileDate
    fileDate = extractFileDateFromName(nameMainPart)
    return fileDate

def isFileImported(db, f, sourceFolder):
    # prueft in der Datenbank db, ob die Datei f aus dem Ordner sourceFolder bereits importiert wurde
    File = Query()
    return len(db.search((File.sourceFile == f) & (File.sourceFolder == sourceFolder))) > 0

def createFolderIfNotExists(newFolder):
    if not os.path.exists(newFolder):
        os.makedirs(newFolder)
    return

def deleteFolderIfExists(folder):
    if os.path.exists(folder):
        print("Verzeichnis >" + folder + "< wird geloescht.")
        shutil.rmtree(folder, ignore_errors=False)
    return

dirMonthArr = ["01 Januar", "02 Februar", "03 Maerz", "04 April", "05 Mai", "06 Juni", "07 Juli", "08 August", "09 September", "10 Oktober", "11 November", "12 Dezember"]

srcDir = str(sys.argv[1]) #"S9PlusJuergen"

print("Auf geht's! srcDir: " + srcDir)

archiveDir = "/media/shuttle/DatenGesichert/private_pictures/testArch"
skpDir = srcDir + "/AlreadyImported"
errDir = srcDir + "/errors"

# cd into scripts directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

deleteFolderIfExists(skpDir)

db = TinyDB("picimport.log.json")

# get list of all source files
fileList = os.listdir(srcDir)

print(str(len(fileList)) + " Dateien im Quell-Verzeichnis >" + srcDir + "< gefunden")

fileList.sort()

for f in fileList:
    if isFileImported(db, f, srcDir):
        createFolderIfNotExists(skpDir)
        os.rename(srcDir + "/" + f, skpDir + "/" + f)
        print("Die Datei >" + f + "< aus Verzeichnis >" + srcDir + "< wurde bereits in der Vergangenheit importiert und jetzt nach >" + skpDir + "< verschoben.")
        continue
    if "." in f:
        nameParts = f.split(".")
        fileExt = "." + nameParts[-1]
        fileMain = nameParts[0]
    else:
        fileExt = ""
        fileMain = f
    print(fileExt)
    imgDate = extractFileDate(srcDir, f, fileMain)
    imgDateStr = imgDate.strftime("%Y_%m_%d_%H_%M_%S")
    print(imgDateStr)
    
    dirYear = "Fotos " + str(imgDate.year)
    
    createFolderIfNotExists(archiveDir + "/" + dirYear)

    dirMonth = dirMonthArr[imgDate.month - 1]

    archiveFinalDir = archiveDir + "/" + dirYear + "/" + dirMonth
    
    createFolderIfNotExists(archiveFinalDir)
    
    sameSecondCounter = 0
    while True:
        fileNew = archiveFinalDir + "/" + imgDateStr + "." + str(sameSecondCounter) + fileExt
        exists = os.path.isfile(fileNew)
        if not exists:
            break
        else:
            print("gibt's schon: " + fileNew)
            sameSecondCounter += 1

    print("Die Datei >" + f + "< aus Verzeichnis >" + srcDir + "< wird als >" + fileNew + "< importiert.")
    os.rename(srcDir + "/" + f, fileNew)

    db.insert({'importtime':datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),'sourceFolder': srcDir, 'sourceFile': f, 'targetFile': fileNew})
