"""Model logic for manual annotation."""

import logging
import pathlib
from typing import Dict, List, Union

import numpy as np
import pandas as pd


class ManualAnnotationModel:
    """Model class for manual annotation tool."""

    def __init__(
        self,
        frame_dict: Dict[int, Dict[str, Union[str, np.ndarray]]],
        df_frames: pd.DataFrame,
        video_name: str,
        src_dir: pathlib.Path,
        classes: List[str],
    ):
        """Initialize model object.

        Args:
            frame_dict: Dictionary with frame images and class information
            df_frames: Dataframe with label information
            video_name: Name of video that frames belong to
            src_dir: Path to root source directory
            classes: Classes in dataset
        """
        self.frame_dict = frame_dict
        self.df_frames = df_frames
        self.video_name = video_name
        self.src_dir = src_dir
        self.classes = classes
        self.class_ind = 0

    def get_frame_indices(self) -> List[int]:
        """Gets available frame indices for video.

        Returns:
            List of frame indices
        """
        return list(self.frame_dict.keys())

    def get_frame_image(self, frame_index: int) -> np.ndarray:
        """Gets image array from specified frame.

        Args:
            frame_index: Frame index to get image from

        Returns:
            Frame image array
        """
        return self.frame_dict[frame_index]["image"]

    def get_frame_class(self, frame_index: int) -> str:
        """Gets class name for specified frame.

        Args:
            frame_index: Frame index to get image from

        Returns:
            Frame class name
        """
        return self.frame_dict[frame_index]["class"]

    def toggle_class(self, frame_index: int) -> None:
        """Toggles class for specified frame.

        Args:
            frame_index: Frame index to get image from
        """
        logger = logging.getLogger(__name__)

        self.class_ind = (self.class_ind + 1) % len(self.classes)

        new_class = self.classes[self.class_ind]

        logger.debug(
            "Toggling Frame %s from %s to %s",
            frame_index,
            self.frame_dict[frame_index]["target"],
            new_class,
        )

        self.frame_dict[frame_index]["target"] = new_class

    def save_video_frames(self) -> None:
        """Saves video frames and metadata to source directory."""
        df_to_update = self.df_frames.loc[self.df_frames["video_name"] == self.video_name, :]

        for frame_ind, f_dict in self.frame_dict.items():
            df_to_update.loc[df_to_update["frame_ind"] == frame_ind, "target"] = f_dict["target"]

        self.df_frames.loc[self.df_frames["video_name"] == self.video_name] = df_to_update
        self.df_frames.to_csv(self.src_dir / "frame_information.csv")
