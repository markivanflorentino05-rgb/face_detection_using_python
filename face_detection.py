import cv2
import os

# 1. Setup
xml_path = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(xml_path)
video_capture = cv2.VideoCapture(0)

# Initialize for Motion Detection
ret, frame1 = video_capture.read()
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

while True:
    ret, frame2 = video_capture.read()
    if not ret: break

    # 2. MOTION DETECTION SENSOR
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    # Calculate difference between frames
    frame_delta = cv2.absdiff(gray1, gray2)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    motion_level = cv2.countNonZero(thresh)

    # 3. FACE TRACKING (Only runs if motion level is high enough)
    # Sensitivity check: 500 is a good starting point
    if motion_level > 500:
        faces = face_cascade.detectMultiScale(gray2, 1.3, 6)

        face_count = len(faces)
        cv2.putText(frame2, f"Status: MOTION DETECTED | Faces: {face_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if face_count > 0:
            cv2.imwrite("captured_face.jpg", frame2)

        # Draw Tracking Circles
        for (x, y, w, h) in faces:
            center_x, center_y = x + w//2, y + h//2
            radius = w // 2
            cv2.circle(frame2, (center_x, center_y), radius, (0, 255, 0), 2)
            cv2.putText(frame2, "TRACKING", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        cv2.putText(frame2, "Status: IDLE", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Smart Tracking System', frame2)

    # Update gray1 for the next comparison
    gray1 = gray2

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()