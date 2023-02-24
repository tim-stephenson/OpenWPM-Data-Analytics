#!/bin/bash

eval "$(micromamba shell hook --shell=bash)"
micromamba activate openwpmdata

cd main
python control.py "$@"