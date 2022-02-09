"""Script for converting file structure to a format that is easier to upload to edge impulse."""
import logging
import pathlib
import shutil

import tqdm
import click

from wai_data_tools.setup_logging import setup_logging


def convert_file_structure_to_upload_format(
    src_root_dir: pathlib.Path, dst_root_dir: pathlib.Path
) -> None:
    """Copy contents of a source file structure and stores it as a format that is easier to upload to edge impulse in a destination directory.

    Args:
        src_root_dir: Source root directory to read files from.
        dst_root_dir: Destination root directory to store new file
            structure.
    """
    frame_dirs = [content for content in src_root_dir.iterdir() if content.is_dir()]

    logging.info("Creating new file structure for uploading to Edge Impulse")
    for frame_dir in tqdm.tqdm(frame_dirs):
        target_dirs = [content for content in frame_dir.iterdir() if content.is_dir()]
        for target_dir in target_dirs:
            target_name = target_dir.stem
            dst_target_dir = dst_root_dir / target_name

            dst_target_dir.mkdir(exist_ok=True, parents=True)

            for frame_filepath in target_dir.glob("*.jpeg"):
                shutil.copy(
                    str(frame_filepath), str(dst_target_dir / frame_filepath.name)
                )


@click.command()
@click.option("--src_root_dir", type=pathlib.Path, help="Source root directory to read images from.")
@click.option("--dst_root_dir", type=pathlib.Path, help="Destination root directory to store new file structure.")
def main(src_root_dir: pathlib.Path,
         dst_root_dir: pathlib.Path) -> None:
    """
    Entrypoint
    """
    setup_logging()
    convert_file_structure_to_upload_format(src_root_dir=src_root_dir,
                                            dst_root_dir=dst_root_dir)


if __name__ == "__main__":
    main()
