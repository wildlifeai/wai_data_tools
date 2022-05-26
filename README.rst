.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://readthedocs.org/projects/wai_data_tools/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://wai_data_tools.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/wai_data_tools/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/wai_data_tools
    .. image:: https://img.shields.io/pypi/v/wai_data_tools.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/wai_data_tools/
    .. image:: https://img.shields.io/conda/vn/conda-forge/wai_data_tools.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/wai_data_tools
    .. image:: https://pepy.tech/badge/wai_data_tools/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/wai_data_tools
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/wai_data_tools

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

==============
Wildlife Watcher Data Tools
==============

Tools and scripts for manipulating the wildlife AI camera data for working with Edge Impulse.

This repository contains good tools for formatting data for the Weta Watcher project.
Typically you would want to use this package if you:
 - Want to format the file structure of your image files
 - Create dataset for Edge impulse image classification models
 - Split video files to image files
 - Re-label incorrect or missing images
 - Apply preprocessing transformations(TODO)
 - Convert structure to a format which is easier to upload to Edge Impulse

==========
Installing
==========

``pip install wai_data_tools``

=====
Usage
=====

Generating a dataset from .mjpg to a new file structure based on labels

``wildlifeai-cli dataset labels create --excel_filepath EXCEL_PATH --raw_data_root_dir YOUR_PATH --dst_root_dir SECOND_PATH``

Generating a dataset of all the frames in the .mjpg and store them as .jpg

``wildlifeai-cli dataset frame create --config_filepath CONFIG_PATH --excel_filepath EXCEL_PATH --src_video_dir YOUR_PATH --dst_frame_dir SECOND_PATH``

Generate a dataset for image classification in edge impulse

``wildlifeai-cli dataset ei create --config-filepath CONFIG_PATH --excel_filepath EXCEL_PATH --src_video_dir YOUR_PATH --dst_root_dir SECOND_PATH``

Converts a dataset to Edge impulse friendly format, from labels structure

``wildlifeai-cli dataset ei import labels --src_root_dir YOUR_PATH --dst_root_dir SECOND_PATH``

Preprocessing via a configfile

``wildlifeai-cli dataset preprocess --config_filepath CONFIG_PATH --src_root_dir YOUR_PATH --dst_root_dir SECOND_PATH``

Filter empty videos from source directory and output in the destination directory

``wildlifeai-cli dataset filter_empty --src_root_dir YOUR_PATH --dst_root_dir SECOND_PATH``

Manually reclassify

``wildlifeai-cli annotate classify --config_filepath CONFIG_PATH --src_root_dir YOUR_PATH --dst_root_dir SECOND_PATH``

.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
