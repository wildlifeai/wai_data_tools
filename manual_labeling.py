

import logging
from pathlib import Path
from typing import Dict, Union

import matplotlib.pyplot as plt
import matplotlib.widgets as pltwid
import numpy as np
import imageio

import setup_logging


def load_frames(frame_dir: Path) -> Dict[int, Dict[str, Union[bool, np.ndarray]]]:
    """
    Loads frame files from a directory.
    :param frame_dir: Path to directory where frames are stored in either a label or no_label folder
    :return: Dictionary where key is frame index and value is a dictionary with the label class and frame image
    """

    logging.info("Loading frames at %s", frame_dir)

    frame_filepaths = frame_dir.rglob("*.jpeg")

    frame_dict = {}

    for frame_filepath in frame_filepaths:

        frame_img = imageio.imread(frame_filepath)

        frame_index = int(frame_filepath.stem.split("___")[-1])

        if frame_filepath.parent.stem not in ["label", "no_label"]:
            raise FileNotFoundError("File structure not recognized. frames should be "
                                    "placed in 'label' and 'no_label' folders")

        if frame_filepath.parent.stem == "label":
            label = True
        else:
            label = False

        logging.info("Frame label class is %s", label)

        frame_dict[frame_index] = {"img": frame_img,
                                   "label": label}
    return frame_dict


class Callbacks:

    def __init__(self,
                 frame_dict: Dict[int, Dict[str, Union[bool, np.ndarray]]],
                 ax_img,
                 ax_togg,
                 frame_dir: Path,
                 new_dir: Path):

        self.frame_dict = frame_dict
        self.frame_dir = frame_dir
        self.new_dir = new_dir
        self.ax_togg = ax_togg
        self.ax_img = ax_img
        self.plt_img = ax_img.imshow(self.frame_dict[0]["img"])
        self.index = 0
        self.max_index = max(self.frame_dict.keys())

    def next(self, event):

        if self.index < self.max_index:
            self.index += 1
        else:
            self.index = 0

        self.draw_img()

    def prev(self, event):

        if self.index > 0:
            self.index -= 1
        else:
            self.index = self.max_index

        self.draw_img()

    def draw_img(self):
        self.plt_img.set_array(self.frame_dict[self.index]["img"])
        self.ax_img.set_title(f"Frame {self.index}")
        self.ax_togg.set_title(f"Class: {self.frame_dict[self.index]['label']}")
        plt.pause(0.001)

    def toggle_label(self, event):
        self.frame_dict[self.index]["label"] = not self.frame_dict[self.index]["label"]
        self.ax_togg.set_title(f"Class: {self.frame_dict[self.index]['label']}")
        plt.pause(0.001)

    def hotkey_press(self, event):
        if event.key == "t":
            self.toggle_label(event=None)
        elif event.key == "left":
            self.prev(event=None)
        elif event.key == "right":
            self.next(event=None)

    def save_frames(self, event):
        video_name = self.frame_dir.stem
        new_video_path = self.new_dir / video_name
        label_dir = new_video_path / "label"
        no_label_dir = new_video_path / "no_label"

        label_dir.mkdir(exist_ok=True, parents=True)
        no_label_dir.mkdir(exist_ok=True, parents=True)

        for frame_ind, f_dict in self.frame_dict.items():
            frame_filename = f"{video_name}___{frame_ind}.jpeg"
            if f_dict["label"]:
                total_path = label_dir / frame_filename
            else:
                total_path = no_label_dir / frame_filename
            imageio.imwrite(total_path, f_dict["img"])
        print("Saved!")


def manual_annotation_plot(frame_dict: Dict[int, Dict[str, Union[bool, np.ndarray]]],
                           frame_dir: Path,
                           new_dir: Path):
    fig, ax = plt.subplots()

    plt.subplots_adjust(bottom=0.2)

    axsave = plt.axes([0.1, 0.05, 0.1, 0.075])
    axtogg = plt.axes([0.5, 0.01, 0.15, 0.075])
    axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.05, 0.1, 0.075])

    bsave = pltwid.Button(axsave, "Save")
    bnext = pltwid.Button(axnext, "Next")
    bprev = pltwid.Button(axprev, "Previous")
    btogg = pltwid.Button(axtogg, "Toggle Class")

    callbacks = Callbacks(frame_dict=frame_dict, ax_img=ax, ax_togg=axtogg, frame_dir=frame_dir, new_dir=new_dir)
    callbacks.draw_img()

    bnext.on_clicked(callbacks.next)
    bprev.on_clicked(callbacks.prev)
    btogg.on_clicked(callbacks.toggle_label)
    bsave.on_clicked(callbacks.save_frames)

    fig.canvas.mpl_connect('key_press_event', callbacks.hotkey_press)

    plt.show()
    

def main():
    setup_logging.setup_logging()
    frame_dir = Path(r"C:\Users\david\Desktop\wildlife.ai\split-test\H_210228_04_00612050")
    new_dir = Path(r"C:\Users\david\Desktop\wildlife.ai\cleaned_dataset")
    frame_dict = load_frames(frame_dir=frame_dir)
    manual_annotation_plot(frame_dict=frame_dict,
                           frame_dir=frame_dir,
                           new_dir=new_dir)


if __name__ == "__main__":
    main()
