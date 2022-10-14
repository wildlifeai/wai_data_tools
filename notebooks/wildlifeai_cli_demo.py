# # Demo for creating edge impulse dataset
# This notebook shows you how to install and use the wai_data_tools package for creating your own dataset to use in Edge Impulse.


# ## Setup

!pip install git+https://github.com/wildlifeai/wai_data_tools.git@install-requirements
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
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Os-cFB7ZJQK-M4BMyfPTWiVE_14H8ddOZyWMtc2isPQ"

# Set this to Path where WW_taranaki_labelled is located in the mounted Drive on Colab.
PATH_TO_RAW_DATA = "/content/drive/MyDrive/WW_taranaki_labelled"

# Set this to your desired output folder on Colab.
PATH_TO_STORE_DATA = "/content/test"

# Run to export the ww_labels sheet to .xlsx format and store it in Colab

sheet = gc.open_by_url(spreadsheet_url)
export_bytes = sheet.export(format="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
PATH_TO_EXCEL = "/content/ww_labels.xlsx"
with open(PATH_TO_EXCEL, 'wb') as export_file:
  export_file.write(export_bytes)

# Create output directory
!mkdir {PATH_TO_STORE_DATA}

# ## Create dataset


!wildlifeai-cli create-ei-dataset --excel_filepath={PATH_TO_EXCEL} --src_video_dir={PATH_TO_RAW_DATA} --dst_root_dir={PATH_TO_STORE_DATA}