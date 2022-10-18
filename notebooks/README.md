# How to work with notebooks and Google Colab

This repo contains a few notebooks used for demos and working using cloud resources in Google Colab. 
In order to store our notebooks in a way that is easier to handle we do not check in notebooks as .ipynb files but as .py files using the [p2j](https://github.com/remykarem/python2jupyter) library.
This requires you to convert the .py files to .ipynb if you want to upload them to Colab.

## How to convert .py file to .ipynb

Run following command where `<path-to-file>` is the path to the .py file you want to convert to .ipynb

``p2j <path-to-file>``

This will create a .ipynb file that you can upload to Colab.

## How to convert .ipynb file to .py file

Run following command where `<path-to-file>` is the path to the .ipynb file you want to convert to .py

``p2j <path-to-file> --reverse``

This will create a .py file that you can check in to the repo.

## Other 
p2j has some extra handy arguments and flags you might want to use. If unsure please run 

``p2j --help``

or read the documentation at [p2j GitHub](https://github.com/remykarem/python2jupyter)