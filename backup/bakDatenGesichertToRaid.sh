#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "bitte mit sudo starten"
  exit
fi

echo "### los gehts ###"

LOGFILE="$0.log"
SECONDS=0

dt=$(date '+%Y-%m-%d %H:%M:%S')

echo "$dt - starte backup" >> $LOGFILE

rsync -rtvP --size-only DatenGesichert/* bakAuto/ShuttleDriveE/

dt=$(date '+%Y-%m-%d %H:%M:%S')

echo "$dt - backup beendet nach $SECONDS sekunden" >> $LOGFILE

echo "### fertig ###"

