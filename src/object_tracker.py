import numpy as np

from typing import Dict, List, Tuple


def update_tracker(
    objects: List[Dict[str, object]],
    tracked_objects: Dict[int, Dict[str, object]],
    next_object_id: int,
    max_distance: float,
    max_history_length: int = 10,
) -> Tuple[Dict[int, Dict[str, object]], int]:
    """Updates the tracker with new objects and updates the age of existing objects.

    Args:
        objects (List[Dict[str, object]]): List of detected objects.
        tracked_objects (Dict[int, Dict[str, object]]): Dictionary of tracked objects.
        next_object_id (int): ID for the next object.
        max_distance (float): Maximum distance for considering an object the same.
        max_history_length (int, optional): Maximum length of the history for an object. Defaults to 10.

    Returns:
        Tuple[Dict[int, Dict[str, object]], int]: Updated tracked objects and next object ID.
    """
    updated_objects: Dict[int, Dict[str, object]] = {}

    # update the age of existing objects
    for obj_id, obj_info in tracked_objects.items():
        obj_info["age"] += 1
        if obj_info["age"] > max_history_length:
            continue
        updated_objects[obj_id] = obj_info

    # new object processing
    for obj in objects:
        closest_id: int = None
        min_distance: float = float("inf")

        for obj_id, tracked_obj in updated_objects.items():
            distance: float = np.linalg.norm(
                np.array(obj["center"]) - np.array(tracked_obj["center"])
            )
            if distance < min_distance:
                min_distance = distance
                closest_id = obj_id

        # If a close object is found, update its data
        if closest_id is not None and min_distance < max_distance:
            tracked_obj = updated_objects[closest_id]
            tracked_obj["center"] = obj["center"]  # new center
            tracked_obj["age"] = 0
            tracked_obj["history"].append(obj["center"])
        else:
            # add a new object if there are no close ones
            updated_objects[next_object_id] = {
                "center": obj["center"],
                "history": [obj["center"]],
                "age": 0,
                "color": [obj["color"]],
                "shape": [obj["shape"]],
            }
            next_object_id += 1

    return updated_objects, next_object_id
