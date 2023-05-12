"""Script for constructing a image dataset by splitting the raw video files into frame images."""
import logging
import pathlib
import shutil
from typing import List, Optional

import cv2
import fiftyone as fo
import pandas as pd
import tqdm
from fiftyone.utils.video import reencode_videos, transform_videos

from wai_data_tools.utils import config_utils, data, read_excel, video_filtering

EI_EXPORT_FORMAT = "edge_impulse"


def filter_empty_videos(src: pathlib.Path, dest: pathlib.Path, dry_run: bool) -> None:
    """Copy all non-empty videos to a folder specified by the user.

    Args:
        src: Path that must already exist with the videos to process
        dest: Path, where to dump the files
        dry_run: boolean
    """
    logger = logging.getLogger(__name__)
    dest.mkdir(parents=True, exist_ok=True)

    for src_file in src.iterdir():
        logger.info("Processing file %s ...", src_file.name)
        is_empty = video_filtering.video_process_content(src_file)
        if not is_empty:
            dest_file = dest / src_file.name
            logger.info("Moving %s to %s", src_file, dest_file)
            if not dry_run:
                shutil.copy(src_file, dest_file)


def create_dataset(
    dataset_name: str, data_dir: pathlib.Path, label_info_path: Optional[pathlib.Path] = None
) -> fo.Dataset:
    """Reads video files and label info into a fiftyone dataset."""
    logger = logging.getLogger(__name__)

    logger.info("Creating a dataset with name %s from content in %s", dataset_name, data_dir)

    logger.info("Renaming files to .mpeg...")
    for mjpg_file in data_dir.glob("*.mjpg"):
        new_name = mjpg_file.parent / f"{mjpg_file.stem}.mpeg"
        mjpg_file.rename(new_name)

    logger.info("Reencoding videos to .mp4...")
    dataset = fo.Dataset.from_dir(dataset_dir=data_dir, dataset_type=fo.types.VideoDirectory, name=dataset_name)
    reencode_videos(dataset, force_reencode=False)
    dataset.compute_metadata()

    logger.info("Removing .mpeg files...")
    for mpeg_file in data_dir.glob("*.mpeg"):
        mpeg_file.unlink()

    if label_info_path:
        logger.info("Adding classifications...")
        content = read_excel.read_excel_to_dataframe(excel_filepath=label_info_path)
        df_labels = read_excel.stack_rows_from_dataframe_dictionary(dataframe_dict=content)
        dataset = _add_classifications(dataset=dataset, df_labels=df_labels)
    dataset.persistent = True
    return dataset


def show_dataset(dataset_name: str) -> None:
    """Get dataset from database."""
    logger = logging.getLogger(__name__)
    logger.info("Launching app for dataset %s ...", dataset_name)
    dataset = fo.load_dataset(dataset_name)
    fo.launch_app(dataset)
    input("Exit? type anything")
    logger.info("Closed app.")


def list_datasets() -> List[str]:
    """List datasets in database."""
    logging.getLogger(__name__).info("Listing datasets...")
    datasets = fo.list_datasets()
    print(datasets)
    return datasets


def export_dataset(
    dataset_name: str,
    export_location: pathlib.Path,
    export_format: str = EI_EXPORT_FORMAT,
    config_filepath: Optional[pathlib.Path] = None,
) -> None:
    """Export a dataset."""
    logger = logging.getLogger(__name__)
    logger.info("Exporting dataset %s to format %s to %s ...", dataset_name, export_format, export_location)
    dataset: fo.Dataset = fo.load_dataset(dataset_name)
    if export_format == EI_EXPORT_FORMAT:
        _export_to_edge_impulse_format(dataset, export_location=export_location, config_filepath=config_filepath)
    else:
        dataset.export(
            export_dir=str(export_location), dataset_type=fo.types.FiftyOneVideoLabelsDataset, export_media=True
        )


def delete_dataset(dataset_name: str) -> None:
    """Delete a dataset in database."""
    logging.getLogger(__name__).info("Removing dataset %s ...", dataset_name)
    fo.delete_dataset(dataset_name, verbose=True)


def create_annotation_job(
    dataset_name: str, anno_key: str, subset: Optional[int] = None, classes: Optional[List[str]] = None
):
    """Create annotation job in CVAT."""
    logger = logging.getLogger(__name__)
    logger.info("Creating annotation job for dataset %s with annotation key %s", dataset_name, anno_key)
    dataset: fo.Dataset = fo.load_dataset(dataset_name)
    if subset:
        logger.info("Taking subset of %s samples from dataset...", subset)
        dataset = dataset.take(subset)
    if classes is None:
        class_set = set()
        for sample in dataset:
            for frame_ind in sample.frames:
                ground_truth = sample.frames[frame_ind].ground_truth
                if ground_truth is not None:
                    class_set.add(ground_truth.label)
        classes = list(class_set)
    logger.info("found classes %s", classes)

    dataset.annotate(anno_key=anno_key, label_field="frames.detections", label_type="detections", classes=classes)


def read_annotations(dataset_name: str, anno_key: str, cleanup: Optional[bool] = False):
    """Read annotations from CVAT."""
    logger = logging.getLogger(__name__)
    logger.info("Reading annotations from CVAT for dataset %s with annotaiton key %s", dataset_name, anno_key)
    dataset: fo.Dataset = fo.load_dataset(dataset_name)
    dataset.load_annotations(anno_key, cleanup=cleanup)


def preprocess_dataset(dataset_name: str, config_filepath: pathlib.Path) -> None:
    """Preprocess dataset to specified fps and size."""
    logger = logging.getLogger(__name__)
    logger.info("Preprocessing dataset %s ...", dataset_name)
    config = config_utils.load_config(config_filepath=config_filepath)
    dataset = fo.load_dataset(dataset_name)
    processing_config = config["transformations"]
    transform_videos(dataset, fps=processing_config["fps"], size=processing_config["size"])


def _add_classifications(dataset: fo.Dataset, df_labels: pd.DataFrame) -> fo.Dataset:
    """Adds classification labels to dataset."""
    logger = logging.getLogger(__name__)
    df_labels["video_name"] = df_labels.apply(lambda row: row.filename.split(".")[0], axis=1)
    for sample in dataset:
        logger.info("Adding classifications for video %s", sample.filepath)
        frame_rate = sample.metadata.frame_rate
        video_name = sample.filepath.split("/")[-1].split(".")[0]

        sample_row = df_labels[df_labels["video_name"] == video_name].iloc[0]

        label = sample_row.label
        label_frame_numbers = data.calculate_frames_in_timespan(
            t_start=sample_row.start, t_end=sample_row.end, fps=frame_rate
        )
        label_frame_numbers += 1
        for frame_number in label_frame_numbers:
            frame = sample[int(frame_number)]
            frame["ground_truth"] = fo.Classification(label=label)
        sample.save()
    return dataset


def _export_to_edge_impulse_format(
    dataset: fo.Dataset, export_location: pathlib.Path, config_filepath: pathlib.Path
) -> None:
    """Export dataset to edge impulse upload format."""
    logger = logging.getLogger(__name__)

    export_location.mkdir(parents=True, exist_ok=True)
    config = config_utils.load_config(config_filepath=config_filepath)
    logger.info("splitting dataset...")
    test_file_inds = data.calc_test_split_indices(
        n_files=len(dataset), test_split_size=config["data_split"]["test_size"]
    )

    for video_ind, video_sample in tqdm.tqdm(enumerate(dataset)):
        split_dir = "test" if video_ind in test_file_inds else "train"

        video = cv2.VideoCapture(video_sample.filepath)  # pylint: disable=no-member

        success = True
        frame_ind = 0
        while success:
            success, frame = video.read()
            if success:
                frame_ind += 1
            else:
                break

            dst_dir = export_location / split_dir
            dst_dir.mkdir(exist_ok=True)

            if video_sample[frame_ind].ground_truth:
                target_name = video_sample[frame_ind].ground_truth.label
            else:
                target_name = "nothing"

            frame_filename = f"{target_name}.{video_sample.filename.split('.')[0]}___{frame_ind}.jpg"
            dst_path = dst_dir / frame_filename
            cv2.imwrite(str(dst_path), frame)  # pylint: disable=no-member
