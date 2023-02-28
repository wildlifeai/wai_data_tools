"""Script for constructing a image dataset by splitting the raw video files into frame images."""
import logging
import pathlib
from typing import List, Optional

import cv2
import fiftyone as fo
import pandas as pd
from fiftyone.utils.video import reencode_videos, transform_videos

from wai_data_tools import config_utils, data, movie_to_images, read_excel


def create_frame_image_dataset(
    excel_filepath: pathlib.Path,
    config_filepath: pathlib.Path,
    src_video_dir: pathlib.Path,
    dst_frame_dir: pathlib.Path,
) -> None:
    """Copy all frames for all .mjpg video files in a directory to a new directory and stores them as jpg files.

    Args:
        excel_filepath: Path to the excel file with label information
        config_filepath: Path to configuration file
        src_video_dir: Path to the source directory containing video files
        dst_frame_dir: Path to the destination root directory to save frame images
    """
    logger = logging.getLogger(__name__)

    logger.info("Reading and formatting excel dataframe")

    content = read_excel.read_excel_to_dataframe(excel_filepath=excel_filepath)

    dataframe = read_excel.stack_rows_from_dataframe_dictionary(dataframe_dict=content)

    dataset_config = config_utils.load_config(config_filepath=config_filepath)
    label_config_list = dataset_config["labels"]
    frame_df = None
    for label_config in label_config_list:
        label_name = label_config["name"]
        logger.info("Processing video files for label %s", label_name)

        label_frame_df = movie_to_images.split_video_files_to_frame_files(
            src_video_dir=src_video_dir,
            video_dataframe=dataframe,
            dst_frame_dir=dst_frame_dir / "dataset",
            label_config=label_config,
        )

        if frame_df is not None:
            frame_df = pd.concat([frame_df, label_frame_df], ignore_index=True)
        else:
            frame_df = label_frame_df

    frame_df.to_csv(dst_frame_dir / "frame_information.csv")


def add_classifications(dataset: fo.Dataset, df_labels: pd.DataFrame) -> fo.Dataset:
    """Adds classification labels to dataset."""
    df_labels["video_name"] = df_labels.apply(lambda row: row.filename.split(".")[0], axis=1)

    for sample in dataset:
        frame_rate = sample.metadata.frame_rate
        video_name = sample.filepath.split("/")[-1].split(".")[0]

        sample_row = df_labels[df_labels["video_name"] == video_name].iloc[0]

        label = sample_row.label
        label_frame_numbers = movie_to_images.calculate_frames_in_timespan(
            t_start=sample_row.start, t_end=sample_row.end, fps=frame_rate
        )
        label_frame_numbers += 1
        for frame_number in label_frame_numbers:
            frame = sample[int(frame_number)]
            frame["ground_truth"] = fo.Classification(label=label)
        sample.save()
    return dataset


def create_dataset(dataset_name: str, data_dir: pathlib.Path, label_info_path: pathlib.Path) -> fo.Dataset:
    """Reads video files and label info into a fiftyone dataset."""
    for mjpg_file in data_dir.glob("*.mjpg"):
        new_name = mjpg_file.parent / f"{mjpg_file.stem}.mpeg"
        mjpg_file.rename(new_name)

    dataset = fo.Dataset.from_dir(dataset_dir=data_dir, dataset_type=fo.types.VideoDirectory, name=dataset_name)
    reencode_videos(dataset, force_reencode=False)
    dataset.compute_metadata()

    for mpeg_file in data_dir.glob("*.mpeg"):
        mpeg_file.unlink()

    content = read_excel.read_excel_to_dataframe(excel_filepath=label_info_path)
    df_labels = read_excel.stack_rows_from_dataframe_dictionary(dataframe_dict=content)
    dataset = add_classifications(dataset=dataset, df_labels=df_labels)
    dataset.persistent = True
    return dataset


def show_dataset(dataset_name: str) -> None:
    """Get dataset from database."""
    dataset = fo.load_dataset(dataset_name)
    fo.launch_app(dataset)
    input("Exit? type anything")


_EI_EXPORT_FORMAT = "edge_impulse"


def export_dataset(
    dataset_name: str,
    export_location: pathlib.Path,
    export_format: str = _EI_EXPORT_FORMAT,
    config_filepath: Optional[pathlib.Path] = None,
) -> None:
    """Export a dataset."""
    dataset: fo.Dataset = fo.load_dataset(dataset_name)
    if export_format == _EI_EXPORT_FORMAT:
        export_to_edge_impulse_format(dataset, export_location=export_location, config_filepath=config_filepath)
    else:
        dataset.export(
            export_dir=str(export_location), dataset_type=fo.types.FiftyOneVideoLabelsDataset, export_media=True
        )


def delete_dataset(dataset_name: str) -> None:
    """Delete a dataset in database."""
    fo.delete_dataset(dataset_name, verbose=True)


def create_annotation_job(dataset_name: str, anno_key: str, subset: Optional[int] = None):
    """Create annotation job in CVAT."""
    dataset: fo.Dataset = fo.load_dataset(dataset_name)
    if subset:
        dataset = dataset.take(subset)
    class_set = set()
    for sample in dataset:
        for frame_ind in sample.frames:
            class_set.add(sample.frames[frame_ind].ground_truth.label)

    dataset.annotate(
        anno_key=anno_key, label_field="frames.detections", label_type="detections", classes=list(class_set)
    )


def read_annotations(dataset_name: str, anno_key: str, cleanup: Optional[bool] = False):
    """Read annotations from CVAT."""
    dataset: fo.Dataset = fo.load_dataset(dataset_name)
    dataset.load_annotations(anno_key, cleanup=cleanup)


def preprocess_dataset(dataset_name: str, config_filepath: pathlib.Path) -> None:
    """Preprocess dataset to specified fps and size."""
    config = config_utils.load_config(config_filepath=config_filepath)
    dataset = fo.load_dataset(dataset_name)
    processing_config = config["transformations"]
    transform_videos(dataset, fps=processing_config["fps"], size=processing_config["size"])


def export_to_edge_impulse_format(
    dataset: fo.Dataset, export_location: pathlib.Path, config_filepath: pathlib.Path
) -> None:
    """Export dataset to edge impulse upload format."""
    export_location.mkdir(parents=True, exist_ok=True)
    config = config_utils.load_config(config_filepath=config_filepath)
    test_file_inds = data.calc_test_split_indices(
        n_files=len(dataset), test_split_size=config["data_split"]["test_size"]
    )

    for video_ind, video_sample in enumerate(dataset):
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


def list_datasets() -> List[str]:
    """List datasets in database."""
    datasets = fo.list_datasets()
    print(datasets)
    return datasets
