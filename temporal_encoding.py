from pathlib import Path

import numpy as np

from manual_labeling import load_frames, save_frames
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt


def temporal_encoding(frame_dicts, processing_config):
    new_frame_dicts = {}

    remove_mean_from_frames(frame_dicts, window_size=40)

    raise AttributeError("hej")

    return new_frame_dicts


def remove_mean_from_frames(frame_dicts, window_size):
    window_inds_dict = get_window_inds(window_size=window_size,
                                       n_frames=len(frame_dicts))

    for (frame_ind, frame_dict), window_inds in zip(frame_dicts.items(), window_inds_dict.values()):
        window_dict = {ind: frame_dicts[ind] for ind in window_inds}
        mean_image = get_voxelwise_mean_for_frames(frame_dicts=window_dict)

        proc_img = frame_dict["img"][:, :, 0].astype(float) - mean_image
        proc_img = np.expand_dims(proc_img, axis=-1)
        proc_img = scale_array_to_8bit(proc_img)
        frame_dict["img"] = np.tile(proc_img, (1, 1, 3))
        display_image(frame_dict["img"])


    pass


def scale_array_to_8bit(img_array):

    img_array += np.abs(np.min(img_array))

    img_array *= (255/np.max(img_array))

    return img_array.astype(int)

def get_window_inds(window_size, n_frames):
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


def get_voxelwise_mean_for_frames(frame_dicts):
    frame_imgs = [frame_dict["img"][:, :, 0].astype(float) for frame_dict in frame_dicts.values()]
    frames_array = np.stack(frame_imgs, axis=0)
    mean_image = np.mean(frames_array, axis=0)
    return mean_image


def display_image(image_array):
    plt.imshow(image_array)
    plt.show()


def create_3_frame_rgb(frame_dicts):
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


data_dir = Path(r"C:\Users\david\Desktop\wildlife.ai\curated-datasets\optimistic-dataset\training")

frame_dirs = list(data_dir.glob("*"))
for frame_dir in frame_dirs:
    print(frame_dir.name)
    frame_dicts = load_frames(frame_dir=frame_dir)

    new_frame_dicts = temporal_encoding(frame_dicts=frame_dicts, processing_config=None)

    save_frames(frame_dir=frame_dir,
                new_dir=Path(r"C:\Users\david\Desktop\wildlife.ai\curated-datasets\temporal-encoding-trials\bg-test"),
                frame_dict=new_frame_dicts)
