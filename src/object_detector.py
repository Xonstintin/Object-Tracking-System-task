from typing import Tuple
import cv2 as cv
import numpy as np


def contours_detection(
    contours: list,
    objects: list,
    mask: np.ndarray,
    image: np.ndarray,
    max_distance: int = 50,
) -> None:
    """Detects objects in a list of contours.

    Args:
        contours (List[np.ndarray]): List of contours to detect objects from.
        objects (list): List of detected objects.
        mask (np.ndarray): Binary mask of the image.
        image (np.ndarray): Image to detect objects from.
        max_distance (int, optional): Maximum distance for an object to be considered. Defaults to 50.
    """
    for contour in contours:
        # determining rectangle for calculating size and coordinates
        x, y, w, h = cv.boundingRect(contour)
        # determining circle for calculating dimensions of circular objects
        (x_center, y_center), radius = cv.minEnclosingCircle(contour)

        center: Tuple[int, int] = (int(x_center), int(y_center))

        # determining the color
        mask_single: np.ndarray = np.zeros_like(mask)
        cv.drawContours(mask_single, [contour], -1, 255, -1)
        mean_val: Tuple[int, int, int] = cv.mean(image, mask=mask_single)
        color: Tuple[int, int, int] = (
            int(mean_val[0]),
            int(mean_val[1]),
            int(mean_val[2]),
        )

        # determining the form
        area: float = cv.contourArea(contour)
        perimeter: float = cv.arcLength(contour, True)
        circularity: float = (
            4 * np.pi * (area / (perimeter * perimeter)) if perimeter != 0 else 0
        )

        if len(cv.approxPolyDP(contour, 0.04 * perimeter, True)) == 4:
            shape: str = "rectangle"
            size: int = w * h
        elif circularity > 0.8:
            shape: str = "circle"
            size: int = int(np.pi * (radius**2))
        else:
            shape: str = "irregular"
            size: int = int(area)
        # add object to list
        if size < max_distance:
            pass
        else:
            objects.append(
                {
                    "center": center,
                    "size": size,
                    "shape": shape,
                    "color": color,
                    "coordinates": (x, y, w, h),
                }
            )


def detect_objects(image: np.ndarray) -> list:
    """Detects objects in an image.

    Args:
        image (np.ndarray): Image to detect objects from.

    Returns:
        list: List of detected objects.
    """
    # image to HSV and mask
    hsv: np.ndarray = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask: np.ndarray = cv.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 30]))
    mask: np.ndarray = cv.bitwise_not(mask)
    # find contours
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    objects = []
    contours_detection(contours, objects, mask, image)
    return objects
