from pathlib import Path

import numpy as np

from manual_labeling import load_frames, save_frames
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt


def temporal_encoding(frame_dicts, window_size=-1):
    new_frame_dicts = {}
    # skip first two because we need two previous frames for encoding
    for frame_ind in range(2, len(frame_dicts)):

        print(frame_ind)
        curr_frame_dict = frame_dicts[frame_ind]
        transformed_im = np.zeros_like(curr_frame_dict["img"]).astype(float)

        # Construct mean and std image

        if window_size == -1:
            window_size = len(frame_dicts)

        seq_arr = np.zeros((transformed_im.shape[0] , transformed_im.shape[1], window_size))

        for window_ind in range(window_size):
            seq_arr[:, :, window_ind] = frame_dicts[window_ind]["img"][:, :, 0]

        mean_im = np.mean(seq_arr, axis=2)

        std_im = np.std(seq_arr, axis=2)

        transformed_im[:, :, 0] = frame_dicts[frame_ind]["img"][:, :, 0]

        tmp = transformed_im[:, :, 0]

        tmp = tmp - mean_im

        tmp = tmp / std_im

        tmp = tmp + abs(np.min(tmp))
        tmp = tmp * 200 / np.max(tmp)
        tmp = tmp.astype(int)

        std_im += abs(std_im)
        std_im *= 200 / np.max(std_im)
        std_im = std_im.astype(int)

        transformed_im[:, :, 1] = tmp
        transformed_im[:, :, 2] = std_im

        plt.imshow(transformed_im.astype(int))
        plt.show()

        raise AttributeError("hej")

        new_frame_dict = {
            "img": transformed_im,
            "label": frame_dicts[frame_ind]["label"]
        }
        new_frame_dicts[frame_ind] = new_frame_dict
    return new_frame_dicts


data_dir = Path(r"C:\Users\david\Desktop\wildlife.ai\curated-datasets\optimistic-dataset\training")

frame_dirs = list(data_dir.glob("*"))
for frame_dir in frame_dirs:
    print(frame_dir.name)
    frame_dicts = load_frames(frame_dir=frame_dir)

    new_frame_dicts = temporal_encoding(frame_dicts=frame_dicts)

    save_frames(frame_dir=frame_dir,
                new_dir=Path(r"C:\Users\david\Desktop\wildlife.ai\curated-datasets\temporal-encoding-trials\bg-test"),
                frame_dict=new_frame_dicts)


s = ""