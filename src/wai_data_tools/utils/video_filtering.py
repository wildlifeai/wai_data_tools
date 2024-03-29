"""This module allows naive processing of videos."""

import itertools
import pathlib

import cv2
import numpy as np


# taken from itertools recipes(exists in 3.10+)
def pairwise(iterable):
    """Creates all tuples that contain an item with its adjacent items.

    Example: s -> (s0,s1), (s1,s2), (s2, s3), ...

    Args:
        iterable: any type of iterable

    Returns:
        generator of the tuples
    """
    op1, op2 = itertools.tee(iterable)
    next(op2, None)
    return zip(op1, op2)


def convert_video_to_frames(src_file: pathlib.Path):
    """Get a video and returns frames.

    Args:
        src_file: full path filename

    Returns:
        list of all frames from the video
    """
    reader = cv2.VideoCapture(str(src_file))  # pylint: disable=no-member
    frames = []
    success = True
    while success:
        success, frame = reader.read()
        frames.append(frame)
    return frames


def check_frames_differences(frames, threshold=50):
    """Return a list of differences between 2 adjacent frames.

    Args:
        frames: List of frames
        threshold: Threshold for activity to use when filtering

    Returns:
        List of differences between any two adjacent frames
    """
    # Ideally this is where a new model would allow to distinguish
    diffs = []
    for frame1, frame2 in pairwise(frames):
        if frame2 is None:
            diff = 0
        else:
            # this gave me surprisingly good results so far
            diff = np.sum(cv2.absdiff(frame1, frame2) >= threshold)  # pylint: disable=no-member
        diffs.append(diff)
    return diffs


def video_process_content(src_file: pathlib.Path, threshold: int = 50) -> bool:
    """Check content of the video and returns if the video is empty.

    Args:
        src_file: full path filename
        threshold: Threshold for activity to use when filtering

    Returns:
        True if video is empty. Otherwise, False.
    """
    frames = convert_video_to_frames(src_file)
    frame_diff = check_frames_differences(frames, threshold=threshold)
    if any(x > 0 for x in frame_diff):
        return False
    return True
