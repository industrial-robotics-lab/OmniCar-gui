
import cv2 as cv


cap = cv.VideoCapture(1)

while True:
    ret, frame = cap.read()
    gry = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    cv.imshow('Cam', gry)
    k = cv.waitKey(5) & 0xFF
    if k == 27:  # esc
        break
# print(ret)
cap.release()
cv.destroyAllWindows()
