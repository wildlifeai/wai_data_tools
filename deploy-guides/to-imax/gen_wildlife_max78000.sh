#!/bin/sh
DEVICE="MAX78000"
CHECKPOINT_FILE="/path/to/checkpoint/file"
NETWORK_CONFIG_FILE="/path/to/network/config/file"
SAMPLE_INPUT_FILE="/path/to/sample/input/file"
TARGET="/path/to/output/dir"
COMMON_ARGS="--device $DEVICE --timer 0 --display-checkpoint --verbose"

python ai8xize.py --test-dir $TARGET --prefix wildlife --checkpoint-file $CHECKPOINT_FILE --config-file $NETWORK_CONFIG_FILE --sample-input $SAMPLE_INPUT_FILE --softmax $COMMON_ARGS "$@"
