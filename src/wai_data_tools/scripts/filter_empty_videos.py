"""This module allows naive processing of videos."""
import itertools
import os
import shutil

import click
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


def convert_video_to_frames(src_file):
    """Get a video and returns frames.

    Args:
        src_file: full path filename

    Returns:
        list of all frames from the video
    """
    reader = cv2.VideoCapture(src_file)
    frames = []
    success = True
    while success:
        success, frame = reader.read()
        frames.append(frame)
    return frames


def check_frames_differences(frames):
    """Return a list of differences between 2 adjacent frames.

    Args:
        frames: List of frames

    Returns:
        List of differences between any two adjacent frames
    """
    # Ideally this is where a new model would allow to distinguish
    diffs = []
    for frame1, frame2 in pairwise(frames):
        if frame2 is None:
            diff = 0
        else:
            diff = np.sum(
                cv2.absdiff(frame1, frame2) >= 50
            )  # this gave me surprisingly good results so far
        diffs.append(diff)
    return diffs


def video_process_content(src_file):
    """Check content of the video and returns if the video is empty.

    Args:
        src_file: full path filename

    Returns:
        True if video is empty. Otherwise, False.
    """
    frames = convert_video_to_frames(src_file)
    frame_diff = check_frames_differences(frames)
    if any(x > 0 for x in frame_diff):
        return False

    return True
