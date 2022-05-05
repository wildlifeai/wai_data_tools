"""Script for preprocessing images in dataset by applying transforms such as resizing, color scale conversions etc."""

import logging
import pathlib

import pandas as pd
import tqdm

from wai_data_tools import config, file_handling, preprocessing


def preprocess_images(
    config_filepath: pathlib.Path,
    src_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Preprocess by applying transformations to images in source directory and store results in destination directory.

    Args:
        config_filepath: Path to config file
        src_root_dir: Source root directory for dataset.
        dst_root_dir: Destination root directory to store processed dataset.
    """
    config_dict = config.load_config(config_filepath=config_filepath)
    preprocess_config = config_dict["preprocessing"]

    logging.info("Composing transforms")
    composed_transforms = preprocessing.compose_transforms(transforms_config=preprocess_config["transformations"])

    logging.info("Preprocessing images")
    df_frames = pd.read_csv(src_root_dir / "frame_information.csv")
    dataset_dir = src_root_dir / "dataset"

    frame_dirs = [dir_path for dir_path in dataset_dir.iterdir() if dir_path.is_dir()]
    for frame_dir in tqdm.tqdm(frame_dirs):
        frames_dict = file_handling.load_frames(frame_dir=frame_dir, df_frames=df_frames)

        for frame_index, frame_dict in frames_dict.items():
            logging.debug(
                "Applying transforms to frame %s for video %s",
                frame_index,
                frame_dir.name,
            )
            frame_dict["image"] = composed_transforms(frame_dict["image"])

        file_handling.save_frames(
            video_name=frame_dir.stem,
            dst_root_dir=dst_root_dir,
            frames_dict=frames_dict,
        )

    df_frames.to_csv(dst_root_dir / "frame_information.csv")
