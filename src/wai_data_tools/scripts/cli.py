"""CLI Group implementation."""

import pathlib

import click

from wai_data_tools.scripts import (
    convert_to_upload_format,
    create_edge_impulse_dataset,
    create_frame_image_dataset,
    create_label_based_data_structure,
    manually_reclassify_frames,
    preprocess_images,
)
from wai_data_tools.setup_logging import setup_logging


@click.group()
def cli() -> None:
    """CLI Tool for creating and transforming datasets."""


@cli.command()
@click.option(
    "--src_root_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the root directory containing the raw Weta Watcher file structure.",
    required=True,
)
@click.option(
    "--dst_root_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the root directory destination to store the label based file structure.",
    required=True,
)
def create_data_structure(
    src_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Copies raw data .mjpg files from the Weta Watcher data file structure to a new file structure based on labels.

    Args:
        src_root_dir: Path to the root directory containing the raw Weta Watcher file structure.
        dst_root_dir: Path to the root directory destination to store the label based file structure.
    """
    setup_logging(logging_dir=dst_root_dir)
    create_label_based_data_structure.create_label_based_file_structure(
        src_root_dir=src_root_dir,
        dst_root_dir=dst_root_dir,
    )


@cli.command()
@click.option(
    "--excel_filepath",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the excel file with label information",
    required=True,
)
@click.option(
    "--config_filepath",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the configuration file",
    required=True,
)
@click.option(
    "--src_video_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the source directory containing video files",
    required=True,
)
@click.option(
    "--dst_frame_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the destination root directory to save frame images",
    required=True,
)
def create_frame_dataset(
    excel_filepath: pathlib.Path,
    config_filepath: pathlib.Path,
    src_video_dir: pathlib.Path,
    dst_frame_dir: pathlib.Path,
) -> None:
    """Copy all frames for all .mjpg video files in a directory to a new directory and stores them as .jpg files.

    Args:
        excel_filepath: Path to the excel file with label information
        config_filepath: Path to configuration file
        src_video_dir: Path to the source directory containing video files
        dst_frame_dir: Path to the destination root directory to save frame images
    """
    setup_logging(logging_dir=dst_frame_dir)
    create_frame_image_dataset.create_frame_image_dataset(
        excel_filepath=excel_filepath,
        config_filepath=config_filepath,
        src_video_dir=src_video_dir,
        dst_frame_dir=dst_frame_dir,
    )


@cli.command()
@click.option(
    "--src_root_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the source root directory to read frame images",
    required=True,
)
@click.option(
    "--config_filepath",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to configuration file",
    required=True,
)
def reclassify_frames(
    src_root_dir: pathlib.Path,
    config_filepath: pathlib.Path,
) -> None:
    """Manually reclassify assigned classes to frame images using a Tkinter GUI.

    Args:
        src_root_dir: Path to the source root directory to read frame images
        config_filepath: Path to configuration file
    """
    setup_logging(logging_dir=src_root_dir)
    manually_reclassify_frames.manually_reclassify_frames(
        src_root_dir=src_root_dir,
        config_filepath=config_filepath,
    )


@cli.command()
@click.option(
    "--config_filepath",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to config file",
    required=True,
)
@click.option(
    "--src_root_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Source root directory to read images from.",
    required=True,
)
@click.option(
    "--dst_root_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Destination root directory to store images.",
    required=True,
)
def preprocess(
    config_filepath: pathlib.Path,
    src_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Preprocess images in source directory and store results in destination directory.

    Args:
        config_filepath: Path to config file
        src_root_dir: Source root directory to read images from.
        dst_root_dir: Destination root directory to store images.
    """
    setup_logging(logging_dir=dst_root_dir)
    preprocess_images.preprocess_images(
        config_filepath=config_filepath,
        src_root_dir=src_root_dir,
        dst_root_dir=dst_root_dir,
    )


@cli.command()
@click.option(
    "--src_root_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Source root directory to read images from.",
    required=True,
)
@click.option(
    "--dst_root_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Destination root directory to store new file structure.",
    required=True,
)
@click.option(
    "--config_filepath",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to configuration file",
    required=True,
)
def to_upload_format(src_root_dir: pathlib.Path, dst_root_dir: pathlib.Path, config_filepath: pathlib.Path) -> None:
    """Copy contents of a source file structure and stores it in upload friendly format in destination directory.

    Args:
        src_root_dir: Source root directory to read files from.
        dst_root_dir: Destination root directory to store new file structure.
        config_filepath: Path to configuration file
    """
    setup_logging(logging_dir=dst_root_dir)
    convert_to_upload_format.convert_file_structure_to_upload_format(
        src_root_dir=src_root_dir, dst_root_dir=dst_root_dir, config_filepath=config_filepath
    )


@cli.command()
@click.option(
    "--excel_filepath",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the excel file with label information",
    required=True,
)
@click.option(
    "--config_filepath",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to configuration file",
    required=True,
)
@click.option(
    "--src_video_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the source directory containing video file",
    required=True,
)
@click.option(
    "--dst_root_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the destination root directory to store dataset and intermediate data",
    required=True,
)
def create_ei_dataset(
    excel_filepath: pathlib.Path,
    config_filepath: pathlib.Path,
    src_video_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Create image dataset for image classification in edge impulse from raw video files.

    Args:
        excel_filepath: Path to the excel file with label information
        config_filepath: Path to configuration file
        src_video_dir: Path to the source directory containing video files
        dst_root_dir: Path to the destination root directory to store dataset and intermediate data
    """
    setup_logging(logging_dir=dst_root_dir)
    create_edge_impulse_dataset.create_edge_impulse_dataset(
        excel_filepath=excel_filepath,
        config_filepath=config_filepath,
        src_video_dir=src_video_dir,
        dst_root_dir=dst_root_dir,
    )


if __name__ == "__main__":
    cli()
