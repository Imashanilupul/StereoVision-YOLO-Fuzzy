import cv2

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

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        print("❌ Camera read failure")
        break

    # Combine frames side by side
    combined = cv2.hconcat([frame1, frame2])

    cv2.imshow("Camera 1 (Left) | Camera 2 (Right)", combined)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release cameras
cap1.release()
cap2.release()
cv2.destroyAllWindows()
