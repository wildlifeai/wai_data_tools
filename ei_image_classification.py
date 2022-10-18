"""Edge Impulse - OpenMV Image Classification Example."""

import os

import sensor  # pylint: disable=import-error
import tf  # pylint: disable=import-error

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE)  # Set pixel format to GRAYSCALE
sensor.set_framesize(sensor.B64X64)  # Set frame size to B64X64 (64x64)
sensor.set_framerate(4)  # Set frame rate to desired frequency in Hz.
sensor.set_windowing((48, 48))  # Set 48x48 window.
sensor.skip_frames(time=2000)  # Let the camera adjust for 2000 ms.

# Set this to the filename of the model you want to use
MODEL_FILE = "ei-rat-float32-backbone-trained.lite"

with open("../../../Users/david/Desktop/wildlife.ai/to-victor-charles/labels.txt") as file:
    labels = [line.rstrip("\n") for line in file]

# Create predictions directory to save predictions results
try:
    os.mkdir("predictions")
except OSError:
    print("directory exists")

# Write header to csv file
with open("./predictions/preds.csv", "a") as f:
    f.write("ind,not rat,rat\n")


# Index counter for keeping track of predictions
INDEX = -1

# Main prediction loop.
# While condition controls how long you will run capture loop.
# Set to True if you want to run forever.
while True:

    INDEX += 1

    img = sensor.snapshot()

    # default settings just do one detection... change them to search the image...
    for obj in tf.classify(MODEL_FILE, img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
        # This combines the labels and confidence values into a list of tuples

        not_rat_confidence, rat_confidence = obj.output()

        # open csv file in append mode and write prediction results
        with open("./predictions/preds.csv", "a") as f:
            f.write("%s,%f,%f\n" % (INDEX, not_rat_confidence, rat_confidence))

        img.save("./predictions/img_%s.jpeg" % INDEX)
