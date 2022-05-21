"""Module for manually relabeling frames using GUI."""
import logging
import pathlib
from typing import Dict, List, Union

import matplotlib.backend_bases
import matplotlib.pyplot as plt
import matplotlib.widgets as pltwid
import numpy as np
import pandas as pd


class Callbacks:
    """Class for handling callbacks for annotation GUI."""

    def __init__(
        self,
        frame_dict: Dict[int, Dict[str, Union[str, np.ndarray]]],
        df_frames: pd.DataFrame,
        video_name: str,
        ax_img: plt.Axes,
        ax_togg: plt.Axes,
        src_dir: pathlib.Path,
        classes: List[str],
    ):
        self.frame_dict = frame_dict
        self.df_frames = df_frames
        self.video_name = video_name
        self.src_dir = src_dir
        self.ax_togg = ax_togg
        self.ax_img = ax_img
        self.plt_img = ax_img.imshow(self.frame_dict[0]["image"])
        self.index = 0
        self.max_index = max(self.frame_dict.keys())
        self.classes = classes
        self.class_ind = 0

    def next(self, _mouse_event: matplotlib.backend_bases.MouseEvent = None):
        """Move to next one.

        Args:
            _mouse_event: ignored
        """
        if self.index < self.max_index:
            self.index += 1
        else:
            self.index = 0

        self.draw_img()

    def prev(self, _mouse_event: matplotlib.backend_bases.MouseEvent = None):
        """Move to previous one.

        Args:
            _mouse_event: ignored
        """
        if self.index > 0:
            self.index -= 1
        else:
            self.index = self.max_index

        self.draw_img()

    def draw_img(self):
        """Handle showing images."""
        self.plt_img.set_array(self.frame_dict[self.index]["image"])
        self.ax_img.set_title(f"Frame {self.index}")
        self.ax_togg.set_title(f"Class: {self.frame_dict[self.index]['target']}")
        plt.pause(0.001)

    def toggle_label(self, _mouse_event: matplotlib.backend_bases.MouseEvent = None):
        """Handle label change.

        Args:
            _mouse_event: ignored
        """
        logger = logging.getLogger(__name__)

        self.class_ind = (self.class_ind + 1) % len(self.classes)

        new_class = self.classes[self.class_ind]

        logger.debug(
            "Toggling Frame %s from %s to %s",
            self.index,
            self.frame_dict[self.index]["target"],
            new_class,
        )

        self.frame_dict[self.index]["target"] = new_class
        self.ax_togg.set_title(f"Class: {self.frame_dict[self.index]['target']}")
        plt.pause(0.001)

    def hotkey_press(self, key_event: matplotlib.backend_bases.KeyEvent):
        """Handle key press.

        Args:
            key_event: key event object
        """
        if key_event.key == "t":
            self.toggle_label()
        elif key_event.key == "left":
            self.prev()
        elif key_event.key == "right":
            self.next()

    def save_frame_information(self, _mouse_event: matplotlib.backend_bases.MouseEvent = None):
        """Save frame information.

        Args:
            _mouse_event: ignored
        """
        df_to_update = self.df_frames.loc[self.df_frames["video_name"] == self.video_name, :]

        for frame_ind, f_dict in self.frame_dict.items():
            df_to_update.loc[df_to_update["frame_ind"] == frame_ind, "target"] = f_dict["target"]

        self.df_frames.loc[self.df_frames["video_name"] == self.video_name] = df_to_update
        self.df_frames.to_csv(self.src_dir / "frame_information.csv")
        self.ax_img.set_title("Saved!")
        plt.pause(0.001)


def manual_annotation_plot(
    frame_dict: Dict[int, Dict[str, Union[bool, np.ndarray]]],
    df_frames: pd.DataFrame,
    video_name: str,
    src_dir: pathlib.Path,
    classes: List[str],
):
    """Manually annotate the specified plot.

    Args:
        frame_dict: Dictionary with frame image arrays. Key is frame index and value is dict with
                    image array and target information.
        df_frames: Dataframe with frame information
        video_name: Name of source video file that frames belong to
        src_dir: Source directory to store updated frame information dataframe
        classes: different labels
    """
    fig, ax_img = plt.subplots()

    plt.subplots_adjust(bottom=0.2)

    axsave = plt.axes([0.1, 0.05, 0.1, 0.075])
    axtogg = plt.axes([0.5, 0.01, 0.15, 0.075])
    axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.05, 0.1, 0.075])

    bsave = pltwid.Button(axsave, "Save")
    bnext = pltwid.Button(axnext, "Next")
    bprev = pltwid.Button(axprev, "Previous")
    btogg = pltwid.Button(axtogg, "Toggle Class")

    callbacks = Callbacks(
        frame_dict=frame_dict,
        df_frames=df_frames,
        video_name=video_name,
        ax_img=ax_img,
        ax_togg=axtogg,
        src_dir=src_dir,
        classes=classes,
    )
    callbacks.draw_img()

    bnext.on_clicked(callbacks.next)
    bprev.on_clicked(callbacks.prev)
    btogg.on_clicked(callbacks.toggle_label)
    bsave.on_clicked(callbacks.save_frame_information)

    fig.canvas.mpl_connect("key_press_event", callbacks.hotkey_press)

    plt.show()
