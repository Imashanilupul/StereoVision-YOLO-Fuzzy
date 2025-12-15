import cv2
from ultralytics import YOLO

# Load YOLO model
print("Loading YOLO model...")
model = YOLO('yolov8n.pt')  # Using YOLOv8 nano for speed (can change to yolov8s.pt, yolov8m.pt, etc.)

# Open two webcam streams
cap1 = cv2.VideoCapture(0)   # First camera
cap2 = cv2.VideoCapture(1)   # Second camera

cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap1.isOpened() or not cap2.isOpened():
    print("❌ Cannot open one or both cameras")
    exit()

print("✅ Both cameras opened successfully")
print("Press 'q' to quit")

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        print("❌ Camera read failure")
        break

    # Run YOLO detection on both frames
    results1 = model(frame1, verbose=False)
    results2 = model(frame2, verbose=False)

    # Draw detection boxes and labels on both frames
    frame1_annotated = results1[0].plot()
    frame2_annotated = results2[0].plot()

    # Combine frames side by side
    combined = cv2.hconcat([frame1_annotated, frame2_annotated])

    cv2.imshow("Camera 1 (Left) | Camera 2 (Right) - YOLO Detection", combined)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release cameras
cap1.release()
cap2.release()
cv2.destroyAllWindows()
