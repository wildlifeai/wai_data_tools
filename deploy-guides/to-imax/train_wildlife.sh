#!/bin/sh
python train.py --lr 0.001  -b 50 --optimizer Adam --epochs 100 --deterministic --compress policies/schedule.yaml --model ai85net5 --dataset WILDLIFE --device MAX78000 --confusion "$@"
