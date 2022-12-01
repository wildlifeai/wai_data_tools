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
To use it simply copy the wildlife example dataloader ``wildlifeai_dataloader.py`` to the datasets folder in the
**ai8x-training** repo and change the value of the ``DATASET_DIR`` variable to the path where your data is stored.
If you don't have data, you can download sample data here(TODO)

### 2. Run train.py command
Models are trained in the Maxim SDK using the ``train.py`` command,
[see this for more information](https://github.com/MaximIntegratedAI/ai8x-training#training-script).
To run an example training you can run the shell script ``train_wildlife.sh`` with the ai8x-training repo root as
working directory which will start training a small classification model.

## Evaluate a model
Once a model has been trained you can evaluate it using the ``train.py`` script as well.
An example command is created in ``evaluate_wildlife.sh`` that you can run with the ai8x-training repo root as
working directory that will evaluate the model. To run it you need to modify it by changing the value of the
``WEIGHT_PATH`` to the path to some stored weights from the training step.

## Generate C library
Once you have the quantized weights you are ready to compile the model to a C library that can be run on the MAX78000
chip, [see here for mor information](https://github.com/MaximIntegratedAI/ai8x-training#network-loader-ai8xize).
To do this you need several things:
- A file with the quantized weights for the model.
- A network config YAML file.
- A sample .npy input file.

### 1. Quantize model weights
When you are happy with your model performance you need to convert it to a C library using the ai8x-synthesis
repository so the model can be run on the MAX78000 chip. This can be done by running the ``quantize.py``command,
[see this for more information](https://github.com/MaximIntegratedAI/ai8x-training#quantization).
An example call is created in ``quantize_wildlife.sh`` that can be used to quantize the weights from your trained model.
To use it you need to set the WEIGHT_PATH and OUTPUT_PATH values to the path to your weights file you want to quantize
and the path where you want to store the quantized weights.

### 2. Generate sample input file
A sample input file can be generated in two ways, either by
[generating a random sample](https://github.com/MaximIntegratedAI/ai8x-training#generating-a-random-sample-input) or by
[saving a sample during training](https://github.com/MaximIntegratedAI/ai8x-training#saving-a-sample-input-from-training-data)

### 3. Generate network config file
Create a network config file using this resource,
[YAML quickstart](https://github.com/MaximIntegratedAI/MaximAI_Documentation/blob/master/Guides/YAML%20Quickstart.md).
The ai8x-synthesis repo has some already created configs that you could also start from.
An example config is created in this repo called ``wildlife-network-config.yaml`` that can be used for small 3D images.

### 4. Compile C library
The compilation is done using the ``ai8xize.py`` command,
[see here for mor information](https://github.com/MaximIntegratedAI/ai8x-training#network-loader-ai8xize).
An example call is created at ``gen_wildlife_max78000.sh`` that can be used. To use it you need to set the paths to
the quantized weight file, sample input file, network config file as well as the output path before running the shell script.
