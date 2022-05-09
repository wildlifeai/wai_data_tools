"""Script for manually reclassifying frames in a frame image dataset."""

import logging
import pathlib

import pandas as pd
import tqdm

import wai_data_tools.io
from wai_data_tools import config, manual_labeling


def manually_reclassify_frames(
    src_root_dir: pathlib.Path,
    config_filepath: pathlib.Path,
) -> None:
    """Manually reclassify assigned classes to frame images using a Tkinter GUI.

    Args:
        src_root_dir: Path to the source root directory to read frame images
        config_filepath: Path to configuration file
    """
    logger = logging.getLogger(__name__)

    logger.info("Reading config file")
    dataset_config = config.load_config(config_filepath=config_filepath)

    classes = [label_config["name"] for label_config in dataset_config["labels"] if label_config["is_target"]]
    classes.append("background")

    logger.info("Found classes %s", classes)

    df_frames = pd.read_csv(src_root_dir / "frame_information.csv")
    dataset_dir = src_root_dir / "dataset"
    logger.info("Starting GUI for reclassification")
    video_dirs = [dir_path for dir_path in dataset_dir.iterdir() if dir_path.is_dir()]
    for video_dir in tqdm.tqdm(video_dirs):
        frames_dict = wai_data_tools.io.load_frames(frame_dir=video_dir, df_frames=df_frames)
        manual_labeling.manual_annotation_plot(
            frame_dict=frames_dict,
            df_frames=df_frames,
            video_name=video_dir.name,
            src_dir=src_root_dir,
            classes=classes,
        )
