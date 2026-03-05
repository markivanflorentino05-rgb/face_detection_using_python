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

    # 2. THE SECURITY FEATURE: Save image if a face is found
    # This saves a file named "face_detected.jpg" in your folder
    if len(faces) > 0:
            cv2.imwrite("captured_face.jpg", frame)

    # Change (255, 0, 0) to (0, 255, 0) for Neon Green
    # Change the thickness from 5 to 2 for a cleaner look
    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Detection System', frame)

    # Press 'q' to quit (or the 'x' button)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()