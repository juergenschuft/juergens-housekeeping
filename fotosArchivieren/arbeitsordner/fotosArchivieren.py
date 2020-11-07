#!/usr/bin/python

import os
import sys
import shutil

from datetime import datetime
from PIL import Image
from PIL import ExifTags
#import time

def skipFile(f, srcDir, errDir):
    createFolderIfNotExists(errDir)
    os.rename(srcDir + "/" + f, errDir + "/" + f)
    print("Fuer Datei >" + f + "< aus Verzeichnis >" + srcDir + "< konnte kein Aufnahmedatum bestimmt werden. Deshalb wurde sie nach >" + errDir + "< verschoben.")
    return

def getExifData(srcDir, fn):
    exifData = {}
    img = Image.open(srcDir + '/' + fn)
    exifDataRaw = img._getexif()
    for tag, value in exifDataRaw.items():
        decodedTag = ExifTags.TAGS.get(tag, tag)
        exifData[decodedTag] = value
    return exifData

def extractFileDateFromName(fn):
    fileDate = None
    # tries to parse fileName fn to dateTime
    datePatterns=["video-%Y-%m-%d-%H-%M-%S", "%Y%m%d_%H%M%S", "%Y_%m_%d_%H_%M_%S", "SL_MO_VID_%Y%m%d_%H%M%S", "VID_%Y%m%d_%H%M%S"]
    patternLenths=[23, 15, 19] # cut away additional chars
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

srcDir = "uploadDir" # str(sys.argv[1]) #"S9PlusJuergen"

print("Auf geht's! srcDir: " + srcDir)

archiveDir = "archiv"
skpDir = os.path.join(srcDir, "AlreadyImported")
errDir = os.path.join(srcDir, "errors")

# cd into scripts directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# deleteFolderIfExists(skpDir)
if os.path.exists(skpDir):
    print("Das Verzeichnis >" + skpDir + "< darf beim Starten des Skriptes nicht existieren.")
    exit()

if os.path.exists(errDir):
    print("Das Verzeichnis >" + errDir + "< darf beim Starten des Skriptes nicht existieren.")
    exit()

# get list of all source files
fileList = os.listdir(srcDir)

print(str(len(fileList)) + " Dateien im Quell-Verzeichnis >" + srcDir + "< gefunden")

fileList.sort()

for f in fileList:
    if f == skpDir:
        continue
    if f == errDir:
        continue
    newFileSize = os.path.getsize(os.path.join(srcDir, f))
    if "." in f:
        nameParts = f.split(".")
        fileExt = "." + nameParts[-1]
        fileMain = nameParts[0]
    else:
        fileExt = ""
        fileMain = f
    print(fileExt)
    imgDate = extractFileDate(srcDir, f, fileMain)
    if imgDate == None:
        skipFile(f, srcDir, errDir)
        continue
    
    imgDateStr = imgDate.strftime("%Y_%m_%d_%H_%M_%S")
    print(imgDateStr)
    
    dirYear = "Fotos " + str(imgDate.year)
    
    createFolderIfNotExists(os.path.join(archiveDir, dirYear))

    dirMonth = dirMonthArr[imgDate.month - 1]

    archiveFinalDir = os.path.join(archiveDir, dirYear, dirMonth) 
    
    createFolderIfNotExists(archiveFinalDir)
    
    sameSecondCounter = 0
    while True:
        skipped = False # geskipped wird, wenn die Daten mit gleichem Namen und gleicher Groesse schon existiert
        fileNew = os.path.join(archiveFinalDir, imgDateStr + "." + str(sameSecondCounter) + fileExt)
        exists = os.path.isfile(fileNew)
        if not exists:
            break
        else:
            existingFileSize = os.path.getsize(fileNew)
            if existingFileSize == newFileSize:
                createFolderIfNotExists(skpDir)
                os.rename(os.path.join(srcDir, f), os.path.join(skpDir, f))
                print("Die Datei >" + f + "< aus Verzeichnis >" + srcDir + "< wurde bereits in der Vergangenheit importiert und jetzt nach >" + skpDir + "< verschoben.")
                skipped = True
                break
            print("gibt's schon: " + fileNew)
            sameSecondCounter += 1
    
    if not skipped:
        print("Die Datei >" + f + "< aus Verzeichnis >" + srcDir + "< wird als >" + fileNew + "< importiert.")
        os.rename(os.path.join(srcDir, f), fileNew)
