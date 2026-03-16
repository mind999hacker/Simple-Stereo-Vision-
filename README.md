# Stereo Vision Distance Estimator

A simple **Python + OpenCV stereo vision system** that estimates the
distance to a target using two cameras. The system works by comparing
the **disparity between camera views** and converting that into
distance.

The workflow is:

1.  Calibrate both cameras to compute focal lengths.
2.  Insert those focal lengths into the main program.
3.  Run the real-time distance estimation.

------------------------------------------------------------------------

# Features

-   Dual camera stereo distance estimation
-   Automatic template matching between cameras
-   Real-time distance display
-   Raw disparity visualization
-   Distance smoothing filter for stable readings
-   Simple calibration process

------------------------------------------------------------------------

# Requirements

Python 3.8+

Install dependencies:

``` bash
pip install opencv-python numpy
```

Hardware:

-   2 USB cameras
-   Cameras mounted horizontally with a fixed baseline
-   A known-size object for calibration (example: license plate)

------------------------------------------------------------------------

# Project Structure

    repo/
    │
    ├── calibration.py   # Tool to compute camera focal lengths
    ├── dist.py          # Main distance estimation program
    └── README.md

------------------------------------------------------------------------

# Step 1 --- Camera Calibration

Before running the main program, you must determine the **focal length
of each camera**.

The calibration script calculates this using a known object size and
distance.

## Setup

Use an object with a **known width**.

Example used in the script:

    KNOWN_WIDTH = 12 inches
    KNOWN_DISTANCE = 24 inches

Place the object exactly **24 inches away from both cameras**.

------------------------------------------------------------------------

## Run Calibration

``` bash
python calibration.py
```

Two windows will open:

    Camera 0
    Camera 2

Instructions:

1.  Hold the object exactly **24 inches from the cameras**
2.  Draw a **tight box across the width of the object**
3.  Release the mouse
4.  The terminal will print the **calculated focal length**

Example output:

    [Camera 0] Pixel Width: 549px | Calculated Focal Length: 1098.00
    [Camera 2] Pixel Width: 676px | Calculated Focal Length: 1352.00

Save these values.

------------------------------------------------------------------------

# Step 2 --- Insert Calibration Values

Open `dist.py`.

Replace the focal length constants:

``` python
FOCAL_CAM0 = 1098.00
FOCAL_CAM2 = 1352.00
```

These values must match your calibration output.

------------------------------------------------------------------------

# Step 3 --- Run Distance Estimation

Run the main program:

``` bash
python dist.py
```

Two windows will appear:

    Camera 0 (Matcher)
    Camera 2 (Target)

Camera 2 contains the **targeting crosshair**.

------------------------------------------------------------------------

# How It Works

### 1. Target Selection

The program takes a small **center patch** from Camera 2.

### 2. Scaling Compensation

The patch is resized using the focal ratio to compensate for different
camera lenses.

### 3. Template Matching

OpenCV searches for the best match in Camera 0 using:

    cv2.matchTemplate()

### 4. Disparity Calculation

Distance is determined by the **horizontal offset** between the target
and the matched region.

    disparity = |match_x - center_x|

### 5. Distance Formula

The system converts disparity into distance using an empirically tuned
function:

    distance = (6800 / (disparity + 45)) - 1

This equation can be tuned depending on camera placement.

------------------------------------------------------------------------

# Output Display

Camera 2 window shows:

    DIST: XX.X in
    RAW DISP: XXX

-   **DIST** = Estimated distance (inches)
-   **RAW DISP** = Raw pixel disparity between cameras

------------------------------------------------------------------------

# Controls

  Key     Action
  ------- --------------
  SPACE   Exit program

------------------------------------------------------------------------

# Camera Setup Recommendations

For best results:

-   Cameras should be **parallel**
-   Cameras should be **level**
-   Mount them **rigidly**
-   Keep a **fixed baseline distance**
-   Use identical resolution settings

Example settings used in code:

    640 x 480 resolution

------------------------------------------------------------------------

# Accuracy Notes

Distance accuracy depends on:

-   calibration precision
-   camera alignment
-   lighting
-   texture on the target
-   baseline distance between cameras

Adding more calibration points can improve the distance model.

------------------------------------------------------------------------

# Possible Improvements

Ideas for improving the project:

-   automatic stereo calibration
-   disparity map generation
-   depth map visualization
-   GPU acceleration
-   object detection tracking
