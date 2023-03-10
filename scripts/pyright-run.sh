#!/bin/bash

if [ -z "$BASH_VERSION" ]; then
    echo "This script is required to be ran with the bash shell via bash SCRIPT"
    exit 1
fi

eval "$(micromamba shell hook --shell=bash)"
micromamba activate openwpmdata

pyright
