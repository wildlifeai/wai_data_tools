from pathlib import Path
from typing import Dict, Union

import numpy as np

from manual_labeling import load_frames, save_frames
import matplotlib.pyplot as plt


def temporal_encoding(frame_dicts: Dict[int, Dict[str, Union[bool, np.ndarray]]], window_size, rgb=False):
    """
    Performs temporal normalizations and encodings for frames dictionary.
    :param frame_dicts:Dictionary where key is frame index and value is a dictionary with the label class
                        and frame image
    :param window_size: Size of sliding window to for voxelwise mean calculation
    :param rgb: boolean if previous frames should be encoded in color channels.
    :return: Modified frames dictionary
    """

    frame_dicts = remove_mean_from_frames(frame_dicts, window_size=window_size)

    if rgb:
        frame_dicts = create_3_frame_rgb(frame_dicts=frame_dicts)

    return frame_dicts


def remove_mean_from_frames(frame_dicts: Dict[int, Dict[str, Union[bool, np.ndarray]]], window_size: int):
    """
    Normalizes each frame by subtracting the mean from a sliding window of specified size.
    :param frame_dicts: Dictionary where key is frame index and value is a dictionary with the label class
                        and frame image
    :param window_size: Size of sliding window
    :return: Modified frames dictionary where mean has been subtracted
    """
    window_inds_dict = calculate_window_inds(window_size=window_size,
                                             n_frames=len(frame_dicts))

    for frame_ind, frame_dict in frame_dicts.items():
        window_dict = {ind: frame_dicts[ind] for ind in window_inds_dict[frame_ind]}
        mean_image = calculate_voxelwise_mean_for_frames(frame_dicts=window_dict)

        proc_img = frame_dict["img"][:, :, 0].astype(float) - mean_image
        proc_img = np.expand_dims(proc_img, axis=-1)
        proc_img = scale_array_to_8bit(proc_img)
        frame_dict["img"] = np.tile(proc_img, (1, 1, 3))
        frame_dict["img"] = frame_dict["img"].astype(np.uint8)
    return frame_dicts


def scale_array_to_8bit(img_array: np.ndarray) -> np.ndarray:
    """
    Scales array values to fit inside uint8 format (0-255)
    :param img_array: image array
    :return: image array scaled and converted to uint8 format
    """

    img_array -= np.min(img_array)

    img_array *= (255/np.max(img_array))

    return img_array.astype(np.uint8)


def calculate_window_inds(window_size: int, n_frames: int) -> Dict[int, np.ndarray]:
    """
    Calculates the frame indices for each window.
    :param window_size: Size of window
    :param n_frames: Total number of frames in sequence
    :return: Dictionary where item is an array of frame indices for a window.
             Key is the frame index that the window is based on
    """
    frame_inds = np.arange(n_frames)
    window_ind_dict = {}
    for frame_ind in frame_inds:

        if frame_ind + window_size <= n_frames:
            start_ind = max(0, np.floor(frame_ind - window_size / 2))
        else:
            start_ind = n_frames - window_size
        end_ind = min(n_frames, start_ind + window_size)
        window_ind_dict[frame_ind] = np.arange(start_ind, end_ind)
    return window_ind_dict


def calculate_voxelwise_mean_for_frames(frame_dicts: Dict[int, Dict[str, Union[bool, np.ndarray]]]) -> np.ndarray:
    """
    calculates the voxelwise mean for the supplied frames
    :param frame_dicts: Dictionary where key is frame index and value is a dictionary with the label class
                        and frame image
    :return: array with voxelwise means for frames
    """
    frame_imgs = [frame_dict["img"][:, :, 0].astype(float) for frame_dict in frame_dicts.values()]
    frames_array = np.stack(frame_imgs, axis=0)
    mean_image = np.mean(frames_array, axis=0)
    return mean_image


def display_image(image_array: np.ndarray):
    """
    Displays an image using matplotlib
    :param image_array: n-dimensional array to show.
    """
    plt.imshow(image_array)
    plt.show()


def create_3_frame_rgb(frame_dicts: Dict[int, Dict[str, Union[bool, np.ndarray]]]):
    new_frame_dicts = {}
    # skip first two because we need two previous frames for encoding
    for curr_frame_ind in range(2, len(frame_dicts)):
        transformed_im = np.zeros_like(frame_dicts[curr_frame_ind]["img"]).astype(float)
        for frame_increment in range(0, 3):
            transformed_im[:, :, frame_increment] = frame_dicts[curr_frame_ind - frame_increment]["img"][:, :, 0]
        new_frame_dict = {
            "img": transformed_im,
            "label": frame_dicts[curr_frame_ind]["label"]
        }
        new_frame_dicts[curr_frame_ind] = new_frame_dict
    return new_frame_dicts


def main():
    data_dir = Path(r"C:\Users\david\Desktop\wildlife.ai\curated-datasets\clean-lens\background-test")

    frame_dirs = list(data_dir.glob("*"))
    for frame_dir in frame_dirs:
        print(frame_dir.name)
        frame_dicts = load_frames(frame_dir=frame_dir)

        new_frame_dicts = temporal_encoding(frame_dicts=frame_dicts, window_size=3)

        save_frames(frame_dir=frame_dir,
                    new_dir=Path(
                        r"C:\Users\david\Desktop\wildlife.ai\curated-datasets\temporal-encoding-trials\ws_3\background-test"),
                    frames_dict=new_frame_dicts)


if __name__ == "__main__":
    main()
