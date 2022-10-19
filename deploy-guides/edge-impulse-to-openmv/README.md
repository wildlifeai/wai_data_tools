# How to deploy an Edge Impulse model to OpenMV

Once you have trained a model and you are happy with results you are ready to deploy the model to the device.
This guide shows you the steps needed to get your model working on the OpenMV chip.
If you have not trained your own model, feel free to clone our pretrained example [rat classification model](https://studio.edgeimpulse.com/public/68936/latest)
for this guide.

## Step 1. Create OpenMV library in Edge Impulse

Go to the **Deployment** page in Edge Impulse and select **OpenMV library** under the **Create library** section.
To create the library press **Build** at the bottom of the page.
When the build is complete it will download a zipped folder with the following contents:

````
ei_image_classification.py - Example script for running your model
labels.txt - Text file with the label names for the model predictions
trained.tflite - File with the image classification model
````

## Step 2. Copy content to device

Next you want to copy the label and model files of the OpenMV library folder to your device.
We have included an alternative to the default example script in this repo with some added functionality.
Copy the ``openmv_image_classification_example.py`` file in the folder where this README is to the device as well.

## Step 3. Modify script with OpenMV editor

## Step 4. Run Model
