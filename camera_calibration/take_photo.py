import cv2
import os

cap = cv2.VideoCapture(0)
COUNT = 1
abs_path = "/home/pi/Documents/omni-platform-python/camera_calibration/"

while True:
    ret, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # img = frame
    
    cv2.imshow('Cam', cv2.flip(img, 0))
    k = cv2.waitKey(5) & 0xFF
    if k == 27:  # esc
        break

    if k == 32:  #space
        rel_path = f"img/{COUNT}.jpeg"
        cv2.imwrite(os.path.join(abs_path, rel_path), img)
        print(f"Saved img {COUNT}")
        COUNT += 1
        
# print(ret)
cap.release()
cv2.destroyAllWindows()
