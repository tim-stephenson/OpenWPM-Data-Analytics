#!/bin/bash

if [ -z "$BASH_VERSION" ]; then
    echo "This script is required to be ran with the bash shell via bash -i SCRIPT"
    exit 1
fi
if [ -z "$PS1" ]; then
    echo "This script is required to be ran interactivly via bash -i SCRIPT"
    exit 1
fi

wget micro.mamba.pm/install.sh -O - | bash -
source ~/.bashrc
echo "successfully installed micromamba $(micromamba --version)"