#!/bin/sh

WEIGHT_PATH="path/to/weights.pth.tar"
OUTPUT_PATH="path/to/store/output.pth.tar"

python quantize.py $WEIGHT_PATH $OUTPUT_PATH --device MAX78000 -v "$@"
