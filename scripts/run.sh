#!/bin/bash

eval "$(micromamba shell hook --shell=bash)"
micromamba activate openwpmdata

pushd main
python control.py "$@"
popd
