# How to train and deploy a model for Maxim MAX78000 chip
This guide will show you an example of how to use the Maxim SDK to train and evaluate a model as well as how to convert
it to a C library for deploying it on the MAX78000 device.

## Setup environment for working with Maxim SDK
Set up your environment according to the guide in SDK documentation here: [Installation](https://github.com/MaximIntegratedAI/ai8x-training#installation)

## Training a model

### 1. Add wildlife.ai dataloader to SDK
In order to train models with new images we need to implement our own custom dataloader
[see this reference fur further information](https://github.com/MaximIntegratedAI/ai8x-training#data-loader).
This repo contains an example implementation for reading data created with the wai_data_tools package.
To use it simply copy the wildlife...

### 2. Run train.py command

## Evaluate a model

## Quantize

## Generate C library
>>>>>>> run-wildlife-maxim-training
