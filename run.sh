#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Requires one arguement: datadir path"
    exit 1
fi

eval "$(micromamba shell hook --shell=bash)"
micromamba activate openwpmdata

cd main
python control.py $1
