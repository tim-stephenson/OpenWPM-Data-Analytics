#!/bin/bash

if [ -z "$BASH_VERSION" ]; then
    echo "This script is required to be ran with the bash shell via bash -i SCRIPT"
    exit 1
fi
if [ -z "$PS1" ]; then
    echo "This script is required to be ran interactivly via bash -i SCRIPT"
    exit 1
fi

micromamba create -f environment.yaml

eval "$(micromamba shell hook --shell=bash)"
micromamba activate openwpmdata

pushd node
npm ci
popd