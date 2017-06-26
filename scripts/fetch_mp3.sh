#! /bin/bash

\rm /tmp/*.mp3
/opt/local/bin/wget -q -O /tmp/$1.mp3 $2 
ls -l /tmp/$1.mp3
