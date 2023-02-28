"""This module is responsible for conversion of the videos to frame by frame format."""
import logging

import numpy as np


def calculate_frames_in_timespan(t_start: float, t_end: float, fps: float) -> np.ndarray:
    """Calculate the frames in the given timespan. Will include one more frame at each end if possible.

    Args:
        t_start: start of time interval in seconds
        t_end: end of time interval in seconds
        fps: frames per second

    Returns:
        array with frame indices
    """
    logger = logging.getLogger(__name__)

    logger.debug("Calculating start and end frame.")

    t_frame = 1 / fps

    frame_start = t_start / t_frame

    if frame_start % 1 > 0:
        logger.debug("Remainder when calculating the index for start frame is not zero. Performing floor operation.")
        frame_start = np.floor(frame_start)

    frame_end = t_end / t_frame

    if frame_end % 1 > 0:
        logger.debug("Remainder when calculating the index for end frame is not zero. Performing ceiling operation.")
        frame_end = np.ceil(frame_end)

    logger.debug("Frames with label start at frame %s and ends at %s", frame_start, frame_end)

    return np.arange(frame_start, frame_end)
