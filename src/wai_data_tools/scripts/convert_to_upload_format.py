"""Script for converting file structure to a format that is easier to upload to edge impulse."""
import logging
import pathlib
import shutil

import tqdm


def convert_file_structure_to_upload_format(
    src_root_dir: pathlib.Path, dst_root_dir: pathlib.Path
) -> None:
    """Copy contents of a source file structure and stores it as a format that is easier to upload to edge impulse in a destination directory.

    Args:
        src_root_dir: Source root directory to read files from.
        dst_root_dir: Destination root directory to store new file structure.
    """
    logger = logging.getLogger(__name__)

    frame_dirs = [content for content in src_root_dir.iterdir() if content.is_dir()]

    logger.info("Creating new file structure for uploading to Edge Impulse")
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
