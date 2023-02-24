#!/bin/bash

wget micro.mamba.pm/install.sh -O - | bash -
source ~/.bashrc
echo "successfully installed micromamba $(micromamba --version)"