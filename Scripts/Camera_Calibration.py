"""
=========================================================
STEREO CAMERA CALIBRATION USING OPENCV
=========================================================

This script performs FULL stereo camera calibration using
a chessboard pattern.

WHAT THIS SCRIPT DOES:
1. Opens left and right cameras
2. Captures synchronized image pairs
3. Detects chessboard corners
4. Calibrates each camera individually
5. Performs stereo calibration
6. Rectifies both cameras
7. Saves all calibration parameters to disk

IMPORTANT:
- DO NOT MOVE cameras after calibration
- Use the SAME resolution during calibration and runtime
- Capture at least 15–25 good image pairs

=========================================================
"""

import cv2
import numpy as np
import os
import time

# --------------------------------------------------------
# USER CONFIGURATION (EDIT THESE)
# --------------------------------------------------------

LEFT_CAM_ID = 0          # Change if needed
RIGHT_CAM_ID = 1         # Change if needed

CHESSBOARD_SIZE = (9, 6) # Number of INNER corners
SQUARE_SIZE = 0.025      # Chessboard square size in meters (e.g. 2.5cm)

NUM_IMAGES = 20          # Minimum 15, recommended 20–25

SAVE_DIR = "calibration_data"
os.makedirs(SAVE_DIR, exist_ok=True)

# --------------------------------------------------------
# TERMINATION CRITERIA FOR CORNER REFINEMENT
# --------------------------------------------------------

criteria = (
    cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
    30,
    0.001
)

# --------------------------------------------------------
# PREPARE 3D OBJECT POINTS (REAL-WORLD COORDINATES)
# --------------------------------------------------------
# Example:
# (0,0,0), (1,0,0), (2,0,0) ... multiplied by square size

objp = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)
objp[:, :2] = np.mgrid[
    0:CHESSBOARD_SIZE[0],
    0:CHESSBOARD_SIZE[1]
].T.reshape(-1, 2)

objp *= SQUARE_SIZE

# Arrays to store object points and image points
objpoints = []       # 3D points in real world space
imgpoints_l = []     # 2D points in left image
imgpoints_r = []     # 2D points in right image

# --------------------------------------------------------
# OPEN CAMERAS
# --------------------------------------------------------

cap_l = cv2.VideoCapture(LEFT_CAM_ID)
cap_r = cv2.VideoCapture(RIGHT_CAM_ID)

if not cap_l.isOpened() or not cap_r.isOpened():
    raise RuntimeError("ERROR: Could not open one or both cameras")

print("\n[INFO] Cameras opened successfully")
print("[INFO] Press 'c' to capture chessboard images")
print("[INFO] Press 'q' to quit\n")

count = 0

# --------------------------------------------------------
# IMAGE CAPTURE LOOP
# --------------------------------------------------------

while count < NUM_IMAGES:
    ret_l, frame_l = cap_l.read()
    ret_r, frame_r = cap_r.read()

    if not ret_l or not ret_r:
        print("[WARNING] Frame capture failed")
        continue

    gray_l = cv2.cvtColor(frame_l, cv2.COLOR_BGR2GRAY)
    gray_r = cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret_l_cb, corners_l = cv2.findChessboardCorners(gray_l, CHESSBOARD_SIZE)
    ret_r_cb, corners_r = cv2.findChessboardCorners(gray_r, CHESSBOARD_SIZE)

    display_l = frame_l.copy()
    display_r = frame_r.copy()

    if ret_l_cb:
        cv2.drawChessboardCorners(display_l, CHESSBOARD_SIZE, corners_l, ret_l_cb)

    if ret_r_cb:
        cv2.drawChessboardCorners(display_r, CHESSBOARD_SIZE, corners_r, ret_r_cb)

    # Show both camera views
    cv2.imshow("Left Camera", display_l)
    cv2.imshow("Right Camera", display_r)

    key = cv2.waitKey(1) & 0xFF

    # ----------------------------------------------------
    # PRESS 'c' TO CAPTURE A VALID IMAGE PAIR
    # ----------------------------------------------------
    if key == ord('c') and ret_l_cb and ret_r_cb:
        print(f"[INFO] Captured pair {count + 1}/{NUM_IMAGES}")

        objpoints.append(objp)

        corners_l = cv2.cornerSubPix(
            gray_l, corners_l, (11, 11), (-1, -1), criteria
        )
        corners_r = cv2.cornerSubPix(
            gray_r, corners_r, (11, 11), (-1, -1), criteria
        )

        imgpoints_l.append(corners_l)
        imgpoints_r.append(corners_r)

        count += 1
        time.sleep(0.5)  # Small delay for stability

    # Quit
    elif key == ord('q'):
        break

# --------------------------------------------------------
# RELEASE CAMERAS
# --------------------------------------------------------

cap_l.release()
cap_r.release()
cv2.destroyAllWindows()

print("\n[INFO] Starting calibration...")

# --------------------------------------------------------
# INDIVIDUAL CAMERA CALIBRATION
# --------------------------------------------------------

ret_l, mtx_l, dist_l, _, _ = cv2.calibrateCamera(
    objpoints, imgpoints_l, gray_l.shape[::-1], None, None
)

ret_r, mtx_r, dist_r, _, _ = cv2.calibrateCamera(
    objpoints, imgpoints_r, gray_r.shape[::-1], None, None
)

print("[INFO] Individual camera calibration done")

# --------------------------------------------------------
# STEREO CALIBRATION
# --------------------------------------------------------

flags = cv2.CALIB_FIX_INTRINSIC

ret, _, _, _, _, R, T, E, F = cv2.stereoCalibrate(
    objpoints,
    imgpoints_l,
    imgpoints_r,
    mtx_l,
    dist_l,
    mtx_r,
    dist_r,
    gray_l.shape[::-1],
    criteria=criteria,
    flags=flags
)

print("[INFO] Stereo calibration done")

# --------------------------------------------------------
# STEREO RECTIFICATION
# --------------------------------------------------------

R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(
    mtx_l,
    dist_l,
    mtx_r,
    dist_r,
    gray_l.shape[::-1],
    R,
    T
)

# --------------------------------------------------------
# SAVE CALIBRATION DATA
# --------------------------------------------------------

np.savez(
    os.path.join(SAVE_DIR, "stereo_calibration.npz"),
    mtx_l=mtx_l,
    dist_l=dist_l,
    mtx_r=mtx_r,
    dist_r=dist_r,
    R=R,
    T=T,
    R1=R1,
    R2=R2,
    P1=P1,
    P2=P2,
    Q=Q
)

baseline = np.linalg.norm(T)
focal_length_px = mtx_l[0, 0]

print("\n================ CALIBRATION RESULTS ================")
print(f"Focal Length (px): {focal_length_px:.2f}")
print(f"Baseline (meters): {baseline:.4f}")
print("Calibration data saved to 'calibration_data/'")
print("====================================================")
