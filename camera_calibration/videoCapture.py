import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gry = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Cam', gry)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:  # esc
        break
# print(ret)
cap.release()
cv2.destroyAllWindows()
