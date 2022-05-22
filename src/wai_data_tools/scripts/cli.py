"""CLI Group implementation."""

import pathlib
import shutil

import click

from wai_data_tools import config, setup_logging
from wai_data_tools.scripts import (
    convert_to_upload_format,
    create_edge_impulse_dataset,
    create_frame_image_dataset,
    create_label_based_data_structure,
    filter_empty_videos,
    manually_reclassify_frames,
    preprocess_images,
)

DEFAULT_CONFIG_PATH = pathlib.Path(__file__).parents[1] / "configs/default_config.yml"


@click.group()
def cli() -> None:
    """CLI Tool for creating and transforming datasets."""


@cli.command()
@click.option(
    "--config_file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to configuration file",
    default=DEFAULT_CONFIG_PATH,
    required=False,
)
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
    config_file: pathlib.Path,
    src_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Copies raw data .mjpg files from the Weta Watcher data file structure to a new file structure based on labels.

    Args:
        config_file: Path to configuration file
        src_root_dir: Path to the root directory containing the raw Weta Watcher file structure.
        dst_root_dir: Path to the root directory destination to store the label based file structure.
    """
    config_dict = config.load_config(config_file=config_file)
    setup_logging.setup_logging(**config_dict["logging"])
    create_label_based_data_structure.create_label_based_file_structure(
        src_root_dir=src_root_dir,
        dst_root_dir=dst_root_dir,
    )


@cli.command()
@click.option(
    "--excel_file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the excel file with label information",
    required=True,
)
@click.option(
    "--config_file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to configuration file",
    default=DEFAULT_CONFIG_PATH,
    required=False,
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
    excel_file: pathlib.Path,
    config_file: pathlib.Path,
    src_video_dir: pathlib.Path,
    dst_frame_dir: pathlib.Path,
) -> None:
    """Copy all frames for all .mjpg video files in a directory to a new directory and stores them as .jpg files.

    Args:
        excel_file: Path to the excel file with label information
        config_file: Path to configuration file
        src_video_dir: Path to the source directory containing video files
        dst_frame_dir: Path to the destination root directory to save frame images
    """
    config_dict = config.load_config(config_file=config_file)
    setup_logging.setup_logging(**config_dict["logging"])

    create_frame_image_dataset.create_frame_image_dataset(
        excel_file=excel_file,
        config_file=config_file,
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
    "--config_file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to configuration file",
    default=DEFAULT_CONFIG_PATH,
    required=False,
)
def reclassify_frames(
    src_root_dir: pathlib.Path,
    config_file: pathlib.Path,
) -> None:
    """Manually reclassify assigned classes to frame images using a Tkinter GUI.

    Args:
        src_root_dir: Path to the source root directory to read frame images
        config_file: Path to configuration file
    """
    config_dict = config.load_config(config_file=config_file)
    setup_logging.setup_logging(**config_dict["logging"])

    manually_reclassify_frames.manually_reclassify_frames(
        src_root_dir=src_root_dir,
        config_file=config_file,
    )


@cli.command()
@click.option(
    "--config_file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to configuration file",
    default=DEFAULT_CONFIG_PATH,
    required=False,
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
    config_file: pathlib.Path,
    src_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Preprocess images in source directory and store results in destination directory.

    Args:
        config_file: Path to config file
        src_root_dir: Source root directory to read images from.
        dst_root_dir: Destination root directory to store images.
    """
    config_dict = config.load_config(config_file=config_file)
    setup_logging.setup_logging(**config_dict["logging"])

    preprocess_images.preprocess_images(
        config_file=config_file,
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
    "--config_file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to config file",
    required=False,
    default=DEFAULT_CONFIG_PATH,
)
def to_upload_format(
    src_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
    config_file: pathlib.Path,
) -> None:
    """Copy contents of dataset to upload friendly structure.

    Copy contents of a source file structure and stores it as a format that is easier to upload to
    edge impulse in a destination directory.

    Args:
        src_root_dir: Source root directory to read files from.
        dst_root_dir: Destination root directory to store new file structure.
        config_file: Path to configuration file
    """
    config_dict = config.load_config(config_file=config_file)
    setup_logging.setup_logging(**config_dict["logging"])
    convert_to_upload_format.convert_file_structure_to_upload_format(
        src_root_dir=src_root_dir, dst_root_dir=dst_root_dir, config_file=config_file
    )


@cli.command()
@click.option(
    "--excel_file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the excel file with label information",
    required=True,
)
@click.option(
    "--config_file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to configuration file",
    default=DEFAULT_CONFIG_PATH,
    required=False,
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
    excel_file: pathlib.Path,
    config_file: pathlib.Path,
    src_video_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Create image dataset for image classification in edge impulse from raw video files.

    Args:
        excel_file: Path to the excel file with label information
        config_file: Path to configuration file
        src_video_dir: Path to the source directory containing video files
        dst_root_dir: Path to the destination root directory to store dataset and intermediate data
    """
    config_dict = config.load_config(config_file=config_file)
    setup_logging.setup_logging(**config_dict["logging"])

    create_edge_impulse_dataset.create_edge_impulse_dataset(
        excel_file=excel_file,
        config_file=config_file,
        src_video_dir=src_video_dir,
        dst_root_dir=dst_root_dir,
    )


@cli.command()
@click.option("--src", default=".", type=click.Path(exists=True))
@click.option("--dest", default="empty_videos", type=click.Path())
@click.option("--dry-run", is_flag=True)
def filter_empty(src: pathlib.Path, dest: pathlib.Path, dry_run: bool) -> None:
    """Copy all non-empty videos to a folder specified by the user.

    Args:
        src: Path that must already exist with the videos to process
        dest: Path, where to dump the files
        dry_run: boolean
    """
    dest.mkdir(parents=True, exist_ok=True)

    for src_file in src.iterdir():
        if src_file.suffix == ".mjpg":
            click.echo(f"Found a non video file named: {src_file.name}")
            continue

        click.echo(f"Processing file {src_file.name} ...")
        is_empty = filter_empty_videos.video_process_content(src_file)
        if not is_empty:
            dest_file = dest / src_file.name
            click.echo(f"Moving {src_file} to {dest_file}")
            if not dry_run:
                shutil.copy(src_file, dest_file)


if __name__ == "__main__":
    cli()
