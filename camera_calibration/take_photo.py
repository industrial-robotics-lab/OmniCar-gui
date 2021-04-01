import cv2

cap = cv2.VideoCapture(0)
COUNT = 100

while True:
    ret, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('Cam', img)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:  # esc
        break

    if k == 32:  #space
        img_name = f"img/{COUNT}.jpeg"
        cv2.imwrite(img_name, img)
        print(f"Saved img {COUNT}")
        COUNT += 1
        
# print(ret)
cap.release()
cv2.destroyAllWindows()
