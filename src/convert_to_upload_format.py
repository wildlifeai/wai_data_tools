"""
Script for converting data structure to a format that is easier for uploading to edge impulse.
"""

from pathlib import Path
import shutil


# Set this to the folder where data is stored.
CURRENT_DATA_DIR = Path(r"C:\Users\david\Desktop\wildlife.ai\curated-datasets\temporal-encoding-trials\rat_rgb_40\test")
# Set this to the folder you want the converted file structure to be stored.
UPLOAD_DATA_DIR = Path(r"C:\Users\david\Desktop\wildlife.ai\to-upload\rat_rgb_40\test")


for frame_dir in CURRENT_DATA_DIR.iterdir():
    label_dir = frame_dir / "label"
    new_label_dir = UPLOAD_DATA_DIR / "label"

    new_label_dir.mkdir(exist_ok=True, parents=True)

    for frame_filepath in label_dir.glob("*.jpeg"):
        shutil.copy(str(frame_filepath), str(new_label_dir / frame_filepath.name))

    no_label_dir = frame_dir / "no_label"
    new_no_label_dir = UPLOAD_DATA_DIR / "no_label"

    new_no_label_dir.mkdir(exist_ok=True, parents=True)

    for frame_filepath in no_label_dir.glob("*.jpeg"):
        shutil.copy(str(frame_filepath), str(new_no_label_dir / frame_filepath.name))
