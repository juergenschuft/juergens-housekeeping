#!/usr/bin/python

import os

from datetime import datetime
from PIL import Image
from PIL import ExifTags
#import time

def getExifData(srcDir, fn):
    exifData = {}
    img = Image.open(srcDir + '/' + fn)
    exifDataRaw = img._getexif()
    for tag, value in exifDataRaw.items():
        decodedTag = ExifTags.TAGS.get(tag, tag)
        exifData[decodedTag] = value
    return exifData

 
def ImageDate(srcDir, fn):
    "Returns the date and time from image(if available)\nfrom Orthallelous"
    TTags=[('DateTimeOriginal','SubsecTimeOriginal'),#when img taken
    ('DateTimeDigitized','SubsecTimeDigitized'),#when img stored digitally
    ('DateTime','SubsecTime')]#when img file was changed
    #for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
    exif=getExifData(srcDir, fn)
    for i in TTags:
        dT, sub = exif.get(i[0]), exif.get(i[1],0)
        dT = dT[0] if type(dT) == tuple else dT#PILLOW 3.0 returns tuples now
        sub = sub[0] if type(sub) == tuple else sub
        if dT!=None:break#got valid time
    if dT==None:return#found no time tags
 
    T=datetime.strptime('{}.{}'.format(dT,sub),'%Y:%m:%d %H:%M:%S.%f')
    #T=time.mktime(time.strptime(dT, '%Y:%m:%d %H:%M:%S')) + float('0.%s'%sub)
    return T

# prüfen, ob work-ordner exisitert - wenn ja, mit fehler abbrechen
# work-ordner anlegen
# dateien aus in-odner umbenennen und in den work-ordner verschieben:
## muster enthält nach sekunden entweder bruchteile (wenn in exif verfügbar) oder zweistellige nummerierung
## 1. dateien mit exif-daten - siehe https://orthallelous.wordpress.com/2015/04/19/extracting-date-and-time-from-images-with-python/
## 2. auf übrige daten (nacheinander alle bekannten) datums-muster anwenden
# bereits existierende bilder der letzten 6 vorhandenen monate (ersten monat merken) und aus old-ordner in work-ordner verschieben & überschreiben
# Ziel-Ordner bis zum aktuellen Datum anlegen
# dateien ab gemerktem monat in Ziel-Ordner verschieben
# work-ordner in "old" umbenennen

print("guten morgen liebe sorgen!")

srcDir = 'lego'
wrkDir = 'work'

fileList = os.listdir(srcDir)
fileList.sort()

for f in fileList:
    if "." in f:
        fileExt = "." + f.split(".")[-1]
    else:
        fileExt = ""
    print(fileExt)
    imgDate = ImageDate(srcDir, f)
    imgDateStr = imgDate.strftime("%Y-%m-%d %H-%M-%S-%f")
    print(imgDateStr)
    fileNew = wrkDir + "/" + imgDateStr + fileExt
    exists = os.path.isfile(fileNew)
    if exists:
        print("gibt's schon: " + fileNew)
    else:
        os.rename(srcDir + "/" + f, fileNew)
