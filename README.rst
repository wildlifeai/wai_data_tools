.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

==============
Wildlife Watcher Data Tools
==============

Tools and scripts for working with datasets captured using the Weta Watcher camera traps.

This repository contains good tools for formatting data for the Weta Watcher project.

Demo can be found here:

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/wildlifeai/wai_data_tools.git/main?labpath=notebooks%2Fwildlifeai_demo.ipynb


==========
Installing
==========

Clone this repo and install it using

``pip install <path-to-repo>``

=====
Usage
=====

You can either use the actions using python functions in scripts or notebooks or run actions using our CLI.

=====
Actions
=====

Supported actions:

- filter_empty_videos: Removes videos where no movement occurs.
- create_dataset: Creates a dataset in FiftyOne.
- show_dataset: Launch FiftyOne App where dataset can be inspected.
- list_datasets: List your datasets.
- create_annotation_job: Send dataset to CVAT for annotation.
- read_annotations: Read annotations from CVAT back to FiftyOne.
- preprocess_dataset: Process dataset to given FPS and size.
- export_dataset: Export dataset to disk in either a FiftyOne format or Edge Impulse.
- delete_dataset: Delete dataset from FiftyOne.

All actions can be found at src/wai_data_tools_actions.py

=====
CLI
=====

To check out the CLI install the package and run the following in your terminal to get started:

``wildlifeai-cli --help``

.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
