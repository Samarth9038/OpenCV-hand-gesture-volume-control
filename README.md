# Gesture Volume Control: Hand-Size Scaled Audio Adjustment

This program utilizes hand gesture recognition with [MediaPipe](https://github.com/google-ai-edge/mediapipe) to control volume. It uses linear regression to dynamically scale the volume based on the user's hand size.

**Key Features:**
* Hand Gesture Recognition: Leverages MediaPipe to track hand movements and identify specific gestures.
* Hand-Size Scaled Control: Adjusts volume based on hand size for a more intuitive and personalized experience.
* Linear Regression: Employs linear regression to establish a smooth and precise relationship between hand size and volume change.

**Possible improvements:**
* Usage of more fitting model eg: Polynomial Regression or Decision Trees.
* Fine-tuning the program to counter Monocular camera view.


  # How to install

  **Note:** Ensure you have Python installed on your system before starting.
  
  **Step-1:** Download the source code from the repository.

  **Step-2:** Create a new folder and extract the downloaded files into it. This will keep your project organized.

  **Step-3:** Run the runMe.bat file to create a virtual environment and install the required dependencies. This ensures that the project's dependencies are isolated from your system-wide Python environment.

  **Step-4:** Once the virtual environment is set up, the runMe.bat file will automatically execute the program. To run the program again, simply execute the runMe.bat file.

  To terminate, close the command prompt window.
