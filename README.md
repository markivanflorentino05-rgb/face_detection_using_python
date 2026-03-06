👤 Face Detection Security System v2.1
A professional Python-based security application that uses OpenCV for real-time motion sensing, facial recognition tracking, and automated event logging.

✨ Key Features
Motion-Triggered Logic: Optimizes performance by only activating face detection when movement is sensed in the frame.

Persistence Buffer: Includes a motion_persistence_buffer to ensure stable tracking even if a subject momentarily stops moving.

Auto-Capture System: Automatically saves high-resolution .jpg logs with unique timestamps to the local /captures directory.

Smart Cooldown: Integrated capture_cooldown_seconds to prevent storage bloat from redundant photos.

🚀 Getting Started
Install Dependencies:
pip install opencv-python

Configuration: Ensure haarcascade_frontalface_default.xml is located in the root directory.

Execution:
python face_detection.py

📂 File Structure
face_detection.py: Main application logic and UI.

.gitignore: Configured to ignore IDE settings and local capture data for a clean repository.

README.md: Project documentation and setup guide.
