#!/bin/sh
if [ "$#" -eq 1 ]
then
micromamba activate openwpmdata
python control.py $1
else
echo "Requires one arguement: datadir path"
exit 1
fi