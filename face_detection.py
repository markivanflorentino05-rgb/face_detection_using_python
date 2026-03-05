import cv2
import os
import time
from datetime import datetime

# 1. Setup
xml_path = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(xml_path)
video_capture = cv2.VideoCapture(0)

if not os.path.exists('captures'):
    os.makedirs('captures')

# SETTINGS & COUNTERS
last_capture_time = 0
cooldown_seconds = 5
motion_buffer = 0  # This prevents the "blinking" UI
threshold_value = 5000 # Higher = less sensitive to noise

# Initialize for Motion Detection
ret, frame1 = video_capture.read()
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

while True:
    ret, frame2 = video_capture.read()
    if not ret: break
    current_time = time.time()

    # 2. MOTION DETECTION
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
    frame_delta = cv2.absdiff(gray1, gray2)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    motion_level = cv2.countNonZero(thresh)

    # 3. MOTION BUFFER LOGIC (The "Anti-Blink" Fix)
    if motion_level > threshold_value:
        motion_buffer = 30  # Keep UI active for 30 frames after motion is seen

    if motion_buffer > 0:
        motion_buffer -= 1 # Countdown the buffer

        faces = face_cascade.detectMultiScale(gray2, 1.3, 6)
        face_count = len(faces)

        cv2.putText(frame2, f"SYSTEM ACTIVE | Faces: {face_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # 4. TIMESTAMPED CAPTURE WITH COOLDOWN
        if face_count > 0 and (current_time - last_capture_time) > cooldown_seconds:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captures/face_{timestamp}.jpg"
            cv2.imwrite(filename, frame2)
            last_capture_time = current_time
            print(f"📸 Captured: {filename}")

        # 5. CYBERPUNK TRACKING UI
        for (x, y, w, h) in faces:
            cx, cy = x + w//2, y + h//2
            cv2.circle(frame2, (cx, cy), w//2, (0, 255, 0), 2)
            cv2.putText(frame2, "TARGET LOCKED", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        cv2.putText(frame2, "Status: MONITORING/IDLE", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Smart Security v2.0', frame2)
    gray1 = gray2

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()