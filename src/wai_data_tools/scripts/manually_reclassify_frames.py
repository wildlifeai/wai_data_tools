"""Script for manually reclassifying frames in a frame image dataset."""

import logging
import pathlib

import click
import tqdm

import wai_data_tools.io
from wai_data_tools import config, manual_labeling, setup_logging


def manually_reclassify_frames(
    src_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
    config_filepath: pathlib.Path,
) -> None:
    """Manually reclassify assigned classes to frame images using a Tkinter GUI.

    Args:
      src_root_dir: Path to the source root directory to read frame images
      dst_root_dir: Path to the destination root directory to save reclassified frame images
      config_filepath: Path to configuration file
    """
    logging.info("Reading config file")
    dataset_config = config.load_config(config_filepath=config_filepath)

    classes = [
        label_config["name"]
        for label_config in dataset_config["labels"]
        if label_config["is_target"]
    ]
    classes.append("background")

    logging.info("Found classes %s", classes)

    logging.info("Starting GUI for reclassification")
    frame_dirs = [dir_path for dir_path in src_root_dir.iterdir() if dir_path.is_dir()]
    for frame_dir in tqdm.tqdm(frame_dirs):
        frames_dict = wai_data_tools.io.load_frames(frame_dir=frame_dir)

        manual_labeling.manual_annotation_plot(
            frame_dict=frames_dict,
            frame_dir=frame_dir,
            dst_root_dir=dst_root_dir,
            classes=classes,
        )


@click.command()
@click.option(
    "--src_root_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the source root directory to read frame images",
)
@click.option(
    "--dst_root_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the destination root directory to save reclassified frame images",
)
@click.option("--config_filepath", type=click.Path(exists=True, path_type=pathlib.Path), help="Path to configuration file")
def main(
    src_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
    config_filepath: pathlib.Path,
) -> None:
    """Entrypoint."""
    setup_logging.setup_logging()
    manually_reclassify_frames(
        src_root_dir=src_root_dir,
        dst_root_dir=dst_root_dir,
        config_filepath=config_filepath,
    )


if __name__ == "__main__":
    main()
