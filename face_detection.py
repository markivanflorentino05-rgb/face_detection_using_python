import cv2
import os
import time
from datetime import datetime

# 1. Setup Configuration
xml_path = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(xml_path)
video_stream = cv2.VideoCapture(0)

# Create directory for saving images if it doesn't exist
if not os.path.exists('captures'):
    os.makedirs('captures')

# Settings & State Tracking
last_capture_timestamp = 0
capture_cooldown_seconds = 5
motion_persistence_buffer = 0  # Prevents UI flickering
motion_sensitivity_threshold = 5000

# Initialize background frame for motion comparison
success, initial_frame = video_stream.read()
previous_gray_frame = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)
previous_gray_frame = cv2.GaussianBlur(previous_gray_frame, (21, 21), 0)

while True:
    success, current_frame = video_stream.read()
    if not success:
        break

    current_unix_time = time.time()

    # 2. Motion Detection Logic
    current_gray_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    current_gray_frame = cv2.GaussianBlur(current_gray_frame, (21, 21), 0)

    # Calculate difference between frames
    frame_delta = cv2.absdiff(previous_gray_frame, current_gray_frame)
    threshold_frame = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    motion_intensity = cv2.countNonZero(threshold_frame)

    # 3. Motion Buffer Management
    if motion_intensity > motion_sensitivity_threshold:
        motion_persistence_buffer = 30  # Active for 30 frames

    if motion_persistence_buffer > 0:
        motion_persistence_buffer -= 1

        detected_faces = face_cascade.detectMultiScale(current_gray_frame, 1.3, 6)
        total_faces = len(detected_faces)

        cv2.putText(current_frame, f"SYSTEM ACTIVE | Faces: {total_faces}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # 4. Automated Image Capture
        time_since_last_capture = current_unix_time - last_capture_timestamp
        if total_faces > 0 and time_since_last_capture > capture_cooldown_seconds:
            file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"captures/face_{file_timestamp}.jpg"

            cv2.imwrite(output_path, current_frame)
            last_capture_timestamp = current_unix_time
            print(f"📸 Security Log Saved: {output_path}")

        # 5. Tracking UI
        for (x_pos, y_pos, width, height) in detected_faces:
            center_x = x_pos + width // 2
            center_y = y_pos + height // 2
            cv2.circle(current_frame, (center_x, center_y), width // 2, (0, 255, 0), 2)
            cv2.putText(current_frame, "TARGET LOCKED", (x_pos, y_pos - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        cv2.putText(current_frame, "Status: MONITORING/IDLE", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Smart Security v2.1', current_frame)
    previous_gray_frame = current_gray_frame

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_stream.release()
cv2.destroyAllWindows()