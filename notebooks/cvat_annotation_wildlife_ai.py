# -*- coding: utf-8 -*-
"""cvat_annotation_wildlife_ai.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Um8387nLlqbeFge8CYsBFvywSGRB-4sJ

# Creating, Inpecting and annotating new Datasets

This notebooks shows you how to create, inspect and annotate new video datasets for the Weta watcher project using the open source platforms [FiftyOne](https://fiftyone.ai) and [CVAT](https://github.com/openvinotoolkit/cvat) which are two leading open-source tools, each tackling different parts of the dataset curation and improvement workflows.

The tight integration between FiftyOne and CVAT allows you to curate and explore datasets in FiftyOne and then send off samples or existing labels for annotation in CVAT with just one line of code.

This colab covers:

* Reading, converting and inspecting new video files using FiftyOne
* Annotating videos using CVAT
* Inspecting annotating results

To Do:
Incorporate filtering for empty videos using wildlife ai tools to only annotate videos with animals

## Setup

Install FiftyOne
"""

# I install the develop branch from fiftyone since the integration with CVAT is broken on current releases
# see issue https://github.com/voxel51/fiftyone/issues/1599
!pip install git+https://github.com/voxel51/fiftyone.git@develop

"""In order to use CVAT, you must create an account on the [cvat website](https://app.cvat.ai). If you haven´t created an account already, please create an account there first and then return to the notebook

### Loading data

We begin by loading a set of unlabeled video files from the test_data folder, this folder does not exist in colab from the start. You will have to find some suitable video files(possibly from the weta watcher drive) and upload them to a folder called test_data
"""

import pathlib

dataset_dir = pathlib.Path("/content/test_data")

"""The file extension .mjpg used for the videos does not really work when reading into fiftyone so here I rename them to .mpeg instead which seems to do the trick."""

# Rename videos to .mpeg format
for mjpg_file in dataset_dir.glob("*.mjpg"):
  new_name = mjpg_file.parent / f"{mjpg_file.stem}.mpeg" 
  mjpg_file.rename(new_name)

"""Load video files into fiftyone"""

# Example
import fiftyone as fo


name = "test_movies"

dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=fo.types.VideoDirectory,
    name=name,
)

"""Reencode videos to .mp4 format for easier handling"""

from fiftyone.utils.video import reencode_videos
reencode_videos(dataset)

"""Now that the data is loaded, let's visualize it in the [FiftyOne App](https://voxel51.com/docs/fiftyone/user_guide/app.html):"""

# the app is broken on develop at the moment. Check this now and then to see if it has been fixed

session = fo.launch_app(dataset)

session.freeze() # screen shot the App for this example

"""## Annotating videos in CVAT

Videos are handled slightly differently by CVAT. For example, each task is only able to contain a single video, so if multiple video samples are uploaded at once via a call to `annotate()`, separate tasks will be created for each video.

Let's upload and annotate 2 samples from the dataset to illustrate the workflow.
"""

# Randomly select 5 samples to load to CVAT
ds_annotate = dataset.take(2)

ds_annotate

anno_key = "vid_anno_1"
ds_annotate.annotate(anno_key, label_type="detections", label_field="frames.detections", classes=["rat"], url="https://app.cvat.ai/")

"""Let's save our annotation work and then load the labels back into FiftyOne."""

ds_annotate.load_annotations(anno_key, cleanup=True)

"""Annotated labels can be reviewed by showing it in the session view or by calling to_dict."""

# Show annotations for first sample in annotation dataset
ds_dict = ds_annotate.first().to_dict(include_frames=True)

for frame_ind, frame_dict in ds_dict["frames"].items():
    if frame_dict["detections"] is None:
      label = "nothing"
    else:
      label = frame_dict["detections"]["detections"][0]["label"]
    print(f"frame {frame_ind} has label {label}")

session.view = ds_annotate
