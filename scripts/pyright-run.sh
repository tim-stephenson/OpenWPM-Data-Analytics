#!/bin/bash

eval "$(micromamba shell hook --shell=bash)"
micromamba activate openwpmdata

pyright
