#!/bin/sh
python quantize.py /Users/davidandersson/git/maxim78000/ai8x-training/logs/2022.11.13-131640/qat_best.pth.tar /Users/davidandersson/git/maxim78000/ai8x-training/logs/2022.11.13-131640/qat_best-q.pth.tar --device MAX78000 -v "$@"
