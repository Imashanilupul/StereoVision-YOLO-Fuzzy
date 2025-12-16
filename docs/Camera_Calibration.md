# Stereo Camera Calibration Instructions

This document provides clear, step-by-step instructions to calibrate two cameras for stereo vision–based distance estimation.

Follow every step carefully to ensure accurate results.

---

## Step 1: Prepare the Chessboard

1. Print a chessboard with **9 × 6 inner corners**
2. Attach it to a **flat, rigid surface**
3. Measure the size of one square using a ruler
4. Convert the square size to meters (example: 25 mm → 0.025 m)
5. Ensure the chessboard is not bent or damaged

---

## Step 2: Mount the Cameras

1. Fix both cameras on a rigid mount
2. Ensure both cameras are:
   - Parallel
   - At the same height
   - Facing straight forward
3. Measure the distance between the camera centers (baseline)
4. Lock the camera positions
5. Do not move the cameras after this step

---

## Step 3: Configure Camera Settings

1. Set both cameras to the same:
   - Resolution
   - Frame rate
2. Disable autofocus if possible
3. Disable auto-exposure if possible
4. Ensure consistent and sufficient lighting

---

## Step 4: Start the Calibration Program

1. Connect both cameras to the computer
2. Run the stereo calibration program
3. Confirm that:
   - Left camera feed is visible
   - Right camera feed is visible
4. Do not adjust camera positions once the program starts

---

## Step 5: Position the Chessboard

1. Hold the chessboard so it is visible in **both cameras**
2. Ensure the entire chessboard appears in both frames
3. Keep the chessboard steady when visible

---

## Step 6: Capture Calibration Image Pairs

Repeat the following steps until **15–25 valid image pairs** are captured:

1. Move the chessboard to different positions:
   - Close to the cameras
   - Far from the cameras
   - Left side of view
   - Right side of view
   - Center of view
2. Tilt the chessboard:
   - Left and right
   - Up and down
3. When both cameras detect the chessboard:
   - Capture the image pair
4. Pause briefly before changing position

Do NOT capture images if:
- The chessboard is partially visible
- The image is blurry
- Only one camera detects the chessboard

---

## Step 7: Finish Image Capture

1. Stop capturing after reaching the required number of image pairs
2. Keep cameras fixed and untouched
3. Allow the program to proceed automatically

---

## Step 8: Calibrate Individual Cameras

1. The program calibrates the left camera
2. The program calibrates the right camera
3. Intrinsic parameters are computed automatically

Do not interrupt this process.

---

## Step 9: Perform Stereo Calibration

1. The program computes:
   - Rotation between cameras
   - Translation between cameras
2. The baseline distance is calculated
3. Stereo camera geometry is established

---

## Step 10: Perform Stereo Rectification

1. The program aligns both camera images horizontally
2. Corresponding points are placed on the same horizontal line
3. Rectification maps are generated

This step is required for accurate disparity calculation.

---

## Step 11: Verify Calibration Quality

1. Display rectified left and right images
2. Observe the same object in both images
3. Confirm that the object lies on the same horizontal line
4. If vertical misalignment is observed:
   - Repeat calibration from Step 6

---

## Step 12: Save Calibration Results

1. Save the calibration parameters:
   - Camera matrices
   - Distortion coefficients
   - Rotation and translation matrices
2. Store the calibration file securely
3. Use these parameters for all distance calculations

---

## Step 13: Rules After Calibration

- Use the same camera resolution during runtime
- Keep cameras fixed at all times
- Do not change camera focus
- Do not move or rotate cameras

---

## Step 14: When to Recalibrate

Recalibration is required if:
- Cameras are moved
- Resolution or frame rate is changed
- Focus is adjusted
- Distance results become unstable

---

## Final Outcome

After completing these steps, the system will be properly calibrated and ready for stereo vision–based distance estimation.
