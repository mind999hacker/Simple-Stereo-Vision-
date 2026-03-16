import cv2
import numpy as np

# --- 1. HARDWARE CALIBRATION ---
FOCAL_CAM0 = 1098.00
FOCAL_CAM2 = 1352.00
SCALE_RATIO = FOCAL_CAM0 / FOCAL_CAM2 

# --- 2. CAMERA SETUP ---
Cam0 = cv2.VideoCapture(0)
Cam2 = cv2.VideoCapture(1)

#forcing similar resolutions, can comment out if using identical cameras
for cam in [Cam0, Cam2]:
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

dist_history = []
box_size = 80  

print("Displaying both Distance and Raw Disparity.")
print("Press [SPACE] to exit.\n")

while True:
    ret0, frame0 = Cam0.read()
    ret2, frame2 = Cam2.read()
    if not (ret0 and ret2): break

    h, w = frame2.shape[:2]
    cx, cy = w // 2, h // 2

    # --- 3. TARGETING & MATCHING ---
    top, bot = cy - box_size // 2, cy + box_size // 2
    left, right = cx - box_size // 2, cx + box_size // 2
    target_patch = frame2[top:bot, left:right]

    # Resize patch to account for lens focal difference
    new_w, new_h = int(box_size * SCALE_RATIO), int(box_size * SCALE_RATIO)
    resized_patch = cv2.resize(target_patch, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Search for match in Camera 0
    gray0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    gray_patch = cv2.cvtColor(resized_patch, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray0, gray_patch, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    # --- 4. CALCULATION & DISPLAY ---
    if max_val > 0.65: 
        match_cx = max_loc[0] + (new_w // 2)
        disparity = abs(match_cx - cx)

        # Apply the fine-tuned formula- Tune it by feeding data into LLM and asking it for better constants
        raw_dist = (6800 / (disparity + 45)) - 1

        # Smoothing filter 
        dist_history.append(raw_dist)
        if len(dist_history) > 8: dist_history.pop(0)
        final_dist = sum(dist_history) / len(dist_history)

        # Draw the match box on Cam 0
        cv2.rectangle(frame0, (max_loc[0], max_loc[1]), 
                      (max_loc[0]+new_w, max_loc[1]+new_h), (0, 255, 0), 2)
        
        # --- DISPLAY DISTANCE AND RAW DISPARITY ---
        cv2.putText(frame2, f"DIST: {final_dist:.1f} in", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        cv2.putText(frame2, f"RAW DISP: {disparity}", (20, 95), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    else:
        cv2.putText(frame2, "AQUIRING TARGET...", (20, 50), 0, 1, (0,0,255), 2)

    # UI Targeting Crosshair
    cv2.rectangle(frame2, (left, top), (right, bot), (0, 255, 255), 2)
    cv2.imshow('Camera 0 (Matcher)', frame0)
    cv2.imshow('Camera 2 (Target)', frame2)

    if cv2.waitKey(1) & 0xFF == ord(' '): break

Cam0.release()
Cam2.release()
cv2.destroyAllWindows()
