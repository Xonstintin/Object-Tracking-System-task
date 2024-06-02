from typing import Dict, List, Tuple, Union
import cv2 as cv
import numpy as np


def visualize_trajectories(
    frame: np.ndarray,
    tracked_objects: Dict[
        int, Dict[str, Union[List[Tuple[int, int]], Tuple[int, int]]]
    ],
) -> None:
    """Draws trajectories and current positions of tracked objects on the video frame.

    Args:
        frame (np.ndarray): The video frame to draw on.
        tracked_objects (Dict[int, Dict[str, Union[List[Tuple[int, int]], Tuple[int, int]]]]): The dictionary of tracked objects.

    Returns:
        None
    """
    for obj_id, obj in tracked_objects.items():
        for i in range(1, len(obj["history"])):
            cv.line(
                frame,
                pt1=obj["history"][i - 1],
                pt2=obj["history"][i],
                color=(0, 255, 0),
                thickness=2,
                lineType=cv.LINE_AA,
            )
        cv.circle(
            img=frame,
            center=obj["center"],
            radius=5,
            color=(0, 255, 0),
            thickness=-1,
            lineType=cv.FILLED,
        )
        cv.putText(
            img=frame,
            text=f"ID {obj_id}",
            org=(obj["center"][0] + 10, obj["center"][1] + 10),
            fontFace=cv.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv.LINE_AA,
        )
