"""Script for preprocessing images in dataset by applying transforms such as resizing, color scale conversions etc."""
import argparse
import logging
import pathlib

import tqdm

from wai_data_tools import config, io, preprocessing
from wai_data_tools.setup_logging import setup_logging


def preprocess_images(
    config_filepath: pathlib.Path,
    src_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Preprocess by applying transformations given in config to images in source directory and store results in destination directory.

    Args:
        config_filepath: Path to config file
        src_root_dir: Source root directory to read images from.
        dst_root_dir: Destination root directory to store images.
    """
    config_dict = config.load_config(config_filepath=config_filepath)
    preprocess_config = config_dict["preprocessing"]

    logging.info("Composing transforms")
    composed_transforms = preprocessing.compose_transforms(
        transforms_config=preprocess_config["transformations"]
    )

    logging.info("Preprocessing images")
    frame_dirs = [dir_path for dir_path in src_root_dir.iterdir() if dir_path.is_dir()]
    for frame_dir in tqdm.tqdm(frame_dirs):
        frames_dict = io.load_frames(frame_dir)

        for frame_index, frame_dict in frames_dict.items():
            logging.debug(
                "Applying transforms to frame %s for video %s",
                frame_index,
                frame_dir.name,
            )
            frame_dict["img"] = composed_transforms(frame_dict["img"])

        io.save_frames(
            video_name=frame_dir.stem,
            dst_root_dir=dst_root_dir,
            frames_dict=frames_dict,
        )


def main():
    """Entrypoint."""
    setup_logging()

    parser = argparse.ArgumentParser(
        "Preprocess all images in given source directory and store results in "
        "destination directory. If source and destination directory is the same, files"
        "will be overwritten"
    )

    parser.add_argument(
        "config_file_path", type=str, help="Path to the configuration file"
    )
    parser.add_argument(
        "src_root_dir",
        type=str,
        help="Path to the root source directory containing image files",
    )
    parser.add_argument(
        "dst_root_dir",
        type=str,
        help="Path to the root destination root directory to save images",
    )

    args = parser.parse_args()

    config_file_path = pathlib.Path(args.config_file_path)
    src_root_dir = pathlib.Path(args.src_root_dir)
    dst_root_dir = pathlib.Path(args.dst_root_dir)

    preprocess_images(
        config_filepath=config_file_path,
        src_root_dir=src_root_dir,
        dst_root_dir=dst_root_dir,
    )


if __name__ == "__main__":
    main()
