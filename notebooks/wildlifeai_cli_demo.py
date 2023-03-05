# # Demo for creating edge impulse dataset
# This notebook shows you how to install and use the wai_data_tools package for creating your own dataset to use in Edge Impulse.

# ## Setup

!pip install git+https://github.com/wildlifeai/wai_data_tools.git@change-to-poetry
!pip install --upgrade gspread --quiet

from google.colab import drive
import gspread
from google.auth import default
from google.colab import auth

# Authenticate to google sheets 

auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# Mount Google Drive to Colab

drive.mount('/content/drive')

# ## Manual Input

# Set spreadsheet_url to URL that points to the ww_labels spreadsheet in the WW_taranaki_labelled folder on drive

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1LtTsPe4X6pwteXx3YDCNbPwjAiyW8v2VQuXCiUU6hys"

# Set this to Path where WW_taranaki_labelled is located in the mounted Drive on Colab.

PATH_TO_RAW_DATA = "/content/drive/MyDrive/ww-demo"

# Set this to your desired output folder on Colab.

PATH_TO_STORE_DATA = "/content/test"

# # Setup

# Run to export the ww_labels sheet to .xlsx format and store it in Colab

sheet = gc.open_by_url(spreadsheet_url)
export_bytes = sheet.export(format="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
PATH_TO_EXCEL = "/content/ww_labels.xlsx"
with open(PATH_TO_EXCEL, 'wb') as export_file:
  export_file.write(export_bytes)

# Create output directory

!mkdir {PATH_TO_STORE_DATA}

# Copy raw data to test folder.

!cp {PATH_TO_RAW_DATA}/*.mjpg {PATH_TO_STORE_DATA}

# # List all commands

!wildlifeai-cli --help

# ## Create dataset

!wildlifeai-cli create-dataset --dataset-name ds1 --data-dir {PATH_TO_STORE_DATA} --label-info-path {PATH_TO_EXCEL}

# # List datasets

!wildlifeai-cli list-datasets

# # Show dataset

import fiftyone

dataset = fiftyone.load_dataset("ds1")
fiftyone.launch_app(dataset)

# # Create config file

!wildlifeai-cli create-config-file --dst ./config.yml

!cat config.yml

# # Create annotation job

!wildlifeai-cli create-annotation-job --dataset-name ds1 --anno-key test

# # Read annotations

!wildlifeai-cli read-annotations --dataset-name ds1 --anno-key test

# # Look at new annotations

import fiftyone

dataset = fiftyone.load_dataset("ds1")
fiftyone.launch_app(dataset)

# # Export dataset

!wildlifeai-cli export-dataset --dataset-name ds1 --dst ./to-export --config-filepath ./config.yml