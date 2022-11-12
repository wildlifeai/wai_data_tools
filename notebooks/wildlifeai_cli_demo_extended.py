# # Extended demo for creating edge impulse dataset
# This notebook will show you how to install and some more available functions for in the wai_data_tools CLI.

# ## Setup

!pip install git+https://github.com/wildlifeai/wai_data_tools.git@install-requirements
!pip install --upgrade gspread --quiet

from pathlib import Path
from google.colab import drive
from google.colab import auth
import gspread
from google.auth import default

# Run to export the ww_labels sheet to .xlsx format
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# Run this to mount drive to the Colab session
drive.mount('/content/drive')

# ## Manual inputs

# Set spreadsheet_url to URL that points to the ww_labels spreadsheet in the WW_taranaki_labelled folder on drive
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Os-cFB7ZJQK-M4BMyfPTWiVE_14H8ddOZyWMtc2isPQ"

# Set this to the path to the root folder containing the raw data
PATH_TO_RAW_DATA = Path("/content/drive/MyDrive/WW_taranaki_labelled")

# Set this to your desired output folder.
PATH_TO_STORE_DATA = Path("/content/frames")

sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1Os-cFB7ZJQK-M4BMyfPTWiVE_14H8ddOZyWMtc2isPQ")
export_bytes = sheet.export(format="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
PATH_TO_EXCEL = "/content/ww_labels.xlsx"
with open(PATH_TO_EXCEL, 'wb') as export_file:
  export_file.write(export_bytes)

# ## CLI commands

!wildlifeai-cli --help

# If you want to configure it a different way you can specify the path to a YAML file
# This cell will copy the default config from the repo to the working dir if you 
# want to experiment with your own configuration.

# TODO add method of getting config

CONFIG_PATH = "../config.yml"
!cp /content/wai_data_tools/src/wai_data_tools/configs/default_config.yml {CONFIG_PATH}

# Create frame dataset from raw data
PATH_TO_STORE_DATA.mkdir(exist_ok=True)
!wildlifeai-cli create-frame-dataset --excel_filepath {PATH_TO_EXCEL} --src_video_dir {PATH_TO_RAW_DATA} --dst_frame_dir {PATH_TO_STORE_DATA} --config_filepath {CONFIG_PATH} 

# This command can be used to reclassify the assigned label to frames using a simple GUI but it does not work on colab.
# !wildlifeai-cli reclassify-frames --src_root_dir {PATH_TO_STORE_DATA} --config_filepath {CONFIG_PATH} 

# Preprocess frame images
!wildlifeai-cli preprocess --config_filepath {CONFIG_PATH} --src_root_dir {PATH_TO_STORE_DATA} --dst_root_dir {PATH_TO_STORE_DATA}

# Copy preprocessed files to upload format
UPLOAD_PATH = PATH_TO_STORE_DATA.parent / "upload"
UPLOAD_PATH.mkdir(exist_ok=True)

!wildlifeai-cli to-upload-format --src_root_dir {PATH_TO_STORE_DATA} --dst_root_dir {UPLOAD_PATH} --config_filepath {CONFIG_PATH}

# Copy preprocessed files to label based directory format
LABEL_PATH = PATH_TO_STORE_DATA.parent / "label-based"
LABEL_PATH.mkdir(exist_ok=True)

!wildlifeai-cli create-data-structure --config_filepath {CONFIG_PATH} --src_root_dir {PATH_TO_STORE_DATA} --dst_root_dir {LABEL_PATH}

