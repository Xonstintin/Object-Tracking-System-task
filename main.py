from src.object_detector import detect_objects, contours_detection
from src.object_trajectory import visualize_trajectories
from src.object_tracker import update_tracker
import cv2


import argparse


def main():
    """
    The main function that runs the video tracking and visualization process.

    Parameters:
    None

    Returns:
    None
    """
    parser = argparse.ArgumentParser(description="Video tracking and visualization")
    parser.add_argument(
        "video_path",
        nargs="?",
        default="data/luxonis_task_video.mp4",
        help="Path to the video file. Defaults to data/luxonis_task_video.mp4",
    )
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.video_path)

    tracked_objects = {}
    next_object_id = 1
    max_distance = 80

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        current_objects = detect_objects(frame)
        # tracker update
        tracked_objects, next_object_id = update_tracker(
            current_objects, tracked_objects, next_object_id, max_distance
        )
        # results visualisation
        visualize_trajectories(frame, tracked_objects)

        # slow
        cv2.waitKey(6)

        cv2.imshow("Tracked", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
