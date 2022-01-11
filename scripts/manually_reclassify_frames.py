"""
Script for manually reclassifying frames in a frame image dataset.
"""

import pathlib
import logging
import argparse

import tqdm

from wai_data_tools import setup_logging
from wai_data_tools import manual_labeling


def manually_reclassify_frames(src_root_dir: pathlib.Path,
                               dst_root_dir: pathlib.Path,
                               configuration_filepath: pathlib.Path) -> None:

    frame_dirs = [dir_path for dir_path in src_root_dir.iterdir() if dir_path.is_dir()]
    for frame_dir in tqdm.tqdm(frame_dirs):
        frames_dict = manual_labeling.load_frames(frame_dir=frame_dir)

        manual_labeling.manual_annotation_plot(frame_dict=frames_dict,
                                               frame_dir=frame_dir,
                                               dst_root_dir=dst_root_dir)


def main():
    setup_logging.setup_logging()


    video_dir = pathlib.Path(r"C:\Users\david\Desktop\wildlife.ai\curated-datasets\rat")
    for frame_dir in video_dir.iterdir():

        new_dir = pathlib.Path(r"C:\Users\david\Desktop\wildlife.ai\curated-datasets\rat-cleaned")

        frame_dict = manual_labeling.load_frames(frame_dir=frame_dir)

        manual_labeling.manual_annotation_plot(frame_dict=frame_dict,
                                               frame_dir=frame_dir,
                                               dst_root_dir=new_dir)


if __name__ == "__main__":
    main()