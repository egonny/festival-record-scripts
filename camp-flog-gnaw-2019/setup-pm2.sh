#!/bin/bash

if [ -z "$1" ]
  then
    echo "No path supplied"
fi

SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`
RECORD_SCRIPT="$SCRIPTPATH/record.py"

pm2 start --name flog-gnaw --interpreter=python3 -o "$1/out.log" -e "$1/err.log" $RECORD_SCRIPT -- --output-dir "$1"