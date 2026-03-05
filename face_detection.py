import cv2
import os

# 1. Setup the Cascade Classifier with a safe path
xml_path = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(xml_path)

# 2. Start the webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Convert to grayscale for the detector
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray_image, 1.3, 6)

    # --- OPTION 1: FACE COUNTER ---
    face_count = len(faces)
    cv2.putText(frame, f"Faces Detected: {face_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 5)

    # Display the resulting frame
    cv2.imshow('Face Detection System', frame)

    # Press 'q' to quit (or the 'x' button)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()