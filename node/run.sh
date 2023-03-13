#!/bin/bash

cd "$(dirname $0)"

eval "$(micromamba shell hook --shell=bash)"
micromamba activate openwpmdata

$@