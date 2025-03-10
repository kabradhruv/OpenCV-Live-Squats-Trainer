# Squat Tracker

Squat Tracker is a Python-based application that uses MediaPipe and OpenCV to detect squats in real time. It provides live feedback on your form, counts repetitions, and is capable of processing both webcam feeds and video file inputs.

## Features

- **Real-Time Pose Detection:** Uses MediaPipe's Pose solution to detect body landmarks.
- **Rep Counting:** Counts squat repetitions based on knee angle thresholds.
- **Live Feedback:** Displays the current knee angle, rep counter, and form feedback directly on the video.
- **Input Options:** Supports both webcam input (default) and video file input.

## Prerequisites

- **Python 3.x**
- **OpenCV:** For video capture and processing.
- **MediaPipe:** For pose estimation.
- **NumPy:** For numerical operations.

## Installation

1. **Clone the repository:**
   ```bash
   https://github.com/kabradhruv/OpenCV-Live-Squats-Trainer.git
   cd squat_tracker
   ```
2. **Install dependencies:**
    ```bash
    pip install opencv-python mediapipe numpy
    ```

3. **Run the script:**
    ```bash
    python squat_tracker.py
    ```

4. **Choose the input source:**
- Uncomment the object witht he file_path as input and replace file_path with your file path to use video file input.
- Or, use the default webcam input by leaving the file_path as None.
