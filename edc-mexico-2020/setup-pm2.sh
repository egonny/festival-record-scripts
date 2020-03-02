#!/bin/bash

if [ -z "$1" ]
  then
    echo "No path supplied"
fi

SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`
RECORD_SCRIPT="$SCRIPTPATH/record.py"

pm2 start --name edc-mexico-1 --log-date-format 'DD-MM HH:mm:ss.SSS' --interpreter=python3 -o "$1/out-1.log" -e "$1/err-1.log" $RECORD_SCRIPT -- 1 --output-dir "$1"