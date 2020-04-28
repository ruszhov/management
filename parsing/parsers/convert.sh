#!/bin/bash

UPLOAD_DIR=$1
HOME=$UPLOAD_DIR
export HOME

#echo `whoami`" home=$HOME"

FILE=$2
#echo $FILE
cd $UPLOAD_DIR
#ls -l $FILE*

libreoffice --headless --convert-to xlsx "$FILE"

#ls -l $FILE*