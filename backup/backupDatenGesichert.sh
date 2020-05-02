#!/bin/bash

# inspiration: https://blog.mdosch.de/2013/08/01/meine-neue-backup-loesung/

if [ "$EUID" -ne 0 ]
  then echo "bitte mit sudo starten"
  exit
fi

echo "### los gehts ###"

LOGFILE="$0.log"
LOGLASTEXEC="lastexec.log"
SECONDS=0

dt=$(date '+%Y-%m-%d %H:%M:%S')

# echo "$dt" # $LOGLASTEXEC

echo "$dt - starte backup" >> $LOGFILE

# rsync -rtvP --size-only --exclude _uploadDir --exclude _fotosArchivieren DatenGesichert/* bakAuto/ShuttleDriveE/

# dt=$(date '+%Y-%m-%d %H:%M:%S')

BAKID="$(date '+%Y%m%d%H%M%S')"

BAKIDLAST="$(<$LOGLASTEXEC)"

echo "BAKID: $BAKID"

echo "BAKIDLAST: $BAKIDLAST"

mkdir "snapshots/$BAKID"

rsync -azvP --delete --size-only --exclude backupman --exclude _uploadDir --exclude _fotosArchivieren --link-dest=../$BAKIDLAST DatenGesichert/* snapshots/$BAKID/ 2>> $LOGFILE

echo "$BAKID" > $LOGLASTEXEC

dt=$(date '+%Y-%m-%d %H:%M:%S')

echo "$dt - backup beendet nach $SECONDS sekunden" >> $LOGFILE

echo "### fertig ###"

