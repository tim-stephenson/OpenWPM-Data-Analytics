#!/bin/sh

cd "$(dirname $0)"

eval "$(conda shell.bash hook)"
conda activate openwpmdata

$@