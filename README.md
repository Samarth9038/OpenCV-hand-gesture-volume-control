# Hand Gesture Volume Control

This project implements a hand gesture-based volume control system using computer vision techniques. It leverages MediaPipe for hand tracking and custom regression models to map hand gestures to volume levels.

## Overview

The system consists of two main phases:

1.  **Data Collection and Model Training:**
    * The `dataCollect` function captures hand gesture data (distance between thumb and index finger) at different levels (closed, half-open, fully open).
    * This data is used to train a polynomial regression model (`regress.py`) that maps the distance to a volume percentage.
    * Outliers are removed from the collected data using the `remOut` function.
    * The trained model weights are saved for later use.
2.  **Real-time Volume Control:**
    * The `run` function uses the trained model to interpret real-time hand gestures.
    * It calculates the distance between the thumb and index finger and uses the regression model to determine the corresponding volume level.
    * The `pyvolume` library is used to set the system volume accordingly.

## Files

* **`main.py`:**
    * Contains the main logic for data collection and real-time volume control.
    * Imports and utilizes `HandTmodule.py` and `regress.py`.
    * Handles user interaction and data processing.
* **`HandTmodule.py`:**
    * Implements hand detection and landmark tracking using MediaPipe.
    * Provides functions to find hand landmarks and calculate distances between them.
* **`regress.py`:**
    * Contains the polynomial regression model and related functions.
    * Handles data standardization, model training (gradient descent), and prediction.
    * Saves and loads the model's weights and other parameters.
* **`pyvolume.py`:**
    * Used to set the system volume.
* **`allData.csv`:**
    * Stores the collected hand gesture data used for model training.
* **`data.npz`:**
    * Stores the trained model parameters (mean, standard deviation, weights, degree).

## Dependencies

* `opencv-python` (`cv2`)
* `mediapipe` (`mp`)
* `time`
* `math`
* `numpy` (`np`)
* `pandas` (`pd`)
* `pyvolume`

## Installation

1.  **Install dependencies:**

    ```bash
    pip install opencv-python mediapipe numpy pandas pyvolume
    ```
    Or just execute the `runMe.bat` file

2.  **Run the data collection and training:**

    ```bash
    python main.py
    ```

    * Follow the on-screen instructions to collect hand gesture data.
    * Press 'y' to start the process, and 'n' to exit the data collection process.
    * Follow the prompts to close, half open, and fully open your index finger and thumb.

3.  **Run the real-time volume control:**

    ```bash
    python main.py
    ```

    * Move your hand to adjust the volume.

## Usage

* The system uses the distance between the thumb and index finger to control the volume.
* Close the fingers to lower the volume, and open them to increase it.
* The system prints out the current volume level to the terminal.

## Customization

* You can adjust the `point` parameter in `main.py` to use different hand landmarks for volume control.
* You can modify the regression model parameters (degree, alpha, iterations) in `regress.py` to improve accuracy.
* You can adjust the threshold value in `remOut` function to change the sensitivity of outlier removal.
* The drawHand and drawPoint bools can be changed to disable or enable the drawing of the hand and points respectively.

## Notes

* The accuracy of the system depends on the quality of the webcam and the lighting conditions.
* The regression model may need to be retrained if the hand gestures or the environment changes significantly.
* The pyvolume library may need to be configured differently on different operating systems.
