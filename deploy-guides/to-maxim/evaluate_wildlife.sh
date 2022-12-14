#!/bin/sh
WEIGHT_PATH="/path/to/weights"

python train.py --model ai85net5 --dataset WILDLIFE --confusion --evaluate --exp-load-weights-from $WEIGHT_PATH --device MAX78000 "$@"
