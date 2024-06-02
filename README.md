# Object Tracking System Documentation

This documentation covers the implementation of an object tracking system designed to detect, track, and visualize moving objects in video feeds. The system utilizes OpenCV for video processing and object detection.

### Structure
```
.
├── data
│   └── luxonis_task_video.mp4
├── main.py
├── README.md
├── requirements.txt
└── src
    ├── object_detector.py
    ├── object_tracker.py
    └── object_trajectory.py

3 directories, 7 files
```


## Dependencies
- OpenCV (cv2): Used for all image processing and video handling tasks.
- NumPy: Utilized for numerical operations especially in managing coordinates and properties of objects.

## Usage
To run this tracking system:

1. Install the required dependencies: `pip install opencv-python numpy` or `pip install -r requirements.txt`
2. Run the `main.py` script with an argument that contains a valid path to a video file. Otherwise it defaults to `data/luxonis_task_video.mp4`
3. Running `-h` is available for quick help.

Note: Make sure you have the necessary video feed available for testing.


## Core Implementation

The script runs in a loop that continuously captures frames from a video feed. For each frame:
1. Objects are detected using the `detect_objects` function.
2. Tracking updates are applied through `update_tracker`, which processes objects based on proximity and updates or initializes tracking data.
3. Object trajectories are visualized using `visualize_trajectories`, which annotates the frames with trajectory lines and object identifiers.

The system leverages several OpenCV functions for image processing, contour detection, and drawing utilities to provide a robust solution for real-time object tracking.


## Modules Description

### object_detector
- **Functionality**: Provides tools to detect objects within a video frame. It converts frames to HSV, applies a threshold to create a mask, detects contours, and identifies objects based on their shapes and colors.
- **Key Functions**:
  - `detect_objects(image)`: Processes an image to detect objects, returning a list of detected objects with properties such as center, size, shape, and color.

### object_trajectory
- **Functionality**: Manages the visualization of object trajectories over time.
- **Key Functions**:
  - `visualize_trajectories(frame, tracked_objects)`: Draws trajectories and current positions of tracked objects on the video frame.

### object_tracker
- **Functionality**: Tracks identified objects across frames, maintaining their state and history.
- **Key Functions**:
  - `update_tracker(objects, tracked_objects, next_object_id, max_distance, max_history_length=10)`: Updates the tracking information for each object, managing new and existing objects, and handling their historical data.
  
## Main and Parameters Description

**Argument Parsing**: Parses command-line arguments to determine the path to the video file.
*   **Video Capture**: Opens the video file for reading using OpenCV's `VideoCapture`.
*   **Initialization**: Initializes variables for tracking objects and setting parameters like `max_distance`.
*   **Frame Processing Loop**:
    *   Reads frames from the video file.
    *   Detects objects in the current frame.
    *   Updates the tracker with the detected objects' information.
    *   Visualizes the trajectories of tracked objects on the frame.
    *   Displays the frame with tracked objects.
    *   Waits for a short period to control the speed of visualization.
    *   Checks for the 'q' keypress to exit the loop.
*   **Cleanup**: Releases the video capture object and destroys OpenCV windows.



### `max_distance`
- **Purpose**: Controls how close two centroids need to be to be considered the same object. It prevents the creation of new IDs for an object that has moved slightly between frames, ensuring the continuity and accuracy of tracking.
- **Typical Usage**: Set based on the expected maximum movement of objects between frames. A lower value can make the tracking more sensitive to movement, potentially leading to multiple IDs for the same object if set too low. Conversely, a very high value might merge separate objects into one if they come close together.
