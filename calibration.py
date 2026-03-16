import cv2

# Known variables
KNOWN_DISTANCE = 24.0 # Inches
KNOWN_WIDTH = 12.0 # Inches (Standard US License Plate)

Cam0 = cv2.VideoCapture(0)
Cam2 = cv2.VideoCapture(1)

drawing = False
ix, iy = -1, -1
cam_id_drawing = -1

def draw_box(event, x, y, flags, param):
    global ix, iy, drawing, cam_id_drawing
    cam_name = param
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        cam_id_drawing = cam_name
        
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        pixel_width = abs(x - ix)
        
        #Math to find Focal Length
        focal_length = (pixel_width * KNOWN_DISTANCE) / KNOWN_WIDTH
        
        print(f"[{cam_name}] Pixel Width: {pixel_width}px | Calculated Focal Length: {focal_length:.2f}")

cv2.namedWindow('Camera 0')
cv2.setMouseCallback('Camera 0', draw_box, param="Camera 0")

cv2.namedWindow('Camera 2')
cv2.setMouseCallback('Camera 2', draw_box, param="Camera 2")

print(f"Place a {KNOWN_WIDTH}-inch object exactly {KNOWN_DISTANCE} inches away.")
print("Draw a tight box around its width in both windows.")
print("Press SPACE to exit.")

while True:
    ret0, frame0 = Cam0.read()
    ret2, frame2 = Cam2.read()
    
    cv2.imshow('Camera 0', frame0)
    cv2.imshow('Camera 2', frame2)
    
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

Cam0.release()
Cam2.release()
cv2.destroyAllWindows()
