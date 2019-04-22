#!/bin/bash

if [ -z "$1" ]
  then
    echo "No path supplied"
fi

SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`
RECORD_SCRIPT="$SCRIPTPATH/record-wk2.py"

pm2 start --name coachella-ch-1 --interpreter=python3 -o "$1/out-1.log" -e "$1/err-1.log" $RECORD_SCRIPT -- 1 --output-dir "$1"
pm2 start --name coachella-ch-2 --interpreter=python3 -o "$1/out-2.log" -e "$1/err-2.log" $RECORD_SCRIPT -- 2 --output-dir "$1"