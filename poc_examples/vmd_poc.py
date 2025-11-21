import cv2
import time
import sys

# --- Configuration ---
# INCREASED: Now requires a much larger object (approx 50x50 pixels) to trigger
MIN_AREA = 2500      
HISTORY = 500        # How many frames to remember for background learning
# INCREASED: Higher value (80) ignores subtle lighting changes/noise better
VAR_THRESHOLD = 400   

def get_camera():
    """
    Opens the camera using standard V4L2 backend.
    """
    print("Attempting to open camera 0 (V4L2)...")
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    
    # Set resolution immediately to 640x480 to reduce memory usage on RPi 5
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    return cap

def main():
    video = get_camera()

    if not video.isOpened():
        print("Error: Could not open video device.")
        return

    print("Camera warming up...")
    time.sleep(1)

    # --- UPGRADE: Background Subtractor MOG2 ---
    # MOG2 is much better than simple frame subtraction. 
    # detectShadows=True helps distinguish shadows from actual objects.
    backSub = cv2.createBackgroundSubtractorMOG2(history=HISTORY, varThreshold=VAR_THRESHOLD, detectShadows=True)

    print("Motion detection started (MOG2 Algo).")
    print(f"Sensitivity Config: Min Area={MIN_AREA}, Threshold={VAR_THRESHOLD}")
    print("Press 'q' to quit.")

    try:
        while True:
            check, frame = video.read()
            if not check:
                break

            # 1. Apply Background Subtractor
            # This creates a mask: Black=Background, White=Motion, Gray=Shadow
            fgMask = backSub.apply(frame)

            # 2. Remove Shadows
            # MOG2 marks shadows as gray (value 127). We threshold to keep only pure white (255).
            # This significantly reduces false positives from shadows.
            _, fgMask = cv2.threshold(fgMask, 250, 255, cv2.THRESH_BINARY)

            # 3. Morphological Operations (Noise Cleaning)
            # "Erode" removes small speckles (noise)
            # "Dilate" makes the remaining white blobs bigger to fill gaps
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            fgMask = cv2.erode(fgMask, kernel, iterations=1)
            fgMask = cv2.dilate(fgMask, kernel, iterations=2)

            # 4. Find Contours on the cleaned mask
            contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            motion_count = 0

            for contour in contours:
                # Filter small movements
                if cv2.contourArea(contour) < MIN_AREA:
                    continue
                
                motion_count += 1
                
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 

            # 5. Status Overlay
            status_text = f"Detected: {motion_count}" if motion_count > 0 else "Idle"
            color = (0, 0, 255) if motion_count > 0 else (0, 255, 0)
            cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # 6. Display
            try:
                cv2.imshow("Motion Detection", frame)
                # cv2.imshow("Mask", fgMask) # Uncomment to see what the computer "sees"
            except cv2.error:
                pass

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        video.release()
        cv2.destroyAllWindows()
        print("Cleaned up.")

if __name__ == "__main__":
    main()
