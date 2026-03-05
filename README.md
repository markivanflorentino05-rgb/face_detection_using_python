# Smart Face Tracking & Security System 🚀

A Python-based computer vision application that uses motion sensing to trigger real-time face detection and automated image capture.

## Key Features
* **Motion Sensor:** Only activates high-power face detection when movement is sensed to save CPU.
* **Cyber-Tracking UI:** Uses neon green circular overlays to track targets in real-time.
* **Auto-Capture:** Automatically saves a `.jpg` of detected faces to the project folder.
* **Sensitivity Tuning:** Easily adjustable motion threshold for different environments.

## How to Run
1.  Install requirements: `pip install opencv-python`
2.  Ensure `haarcascade_frontalface_default.xml` is in the root folder.
3.  Run the script: `python face_detection.py`
4.  Press **'q'** to exit the system safely.
