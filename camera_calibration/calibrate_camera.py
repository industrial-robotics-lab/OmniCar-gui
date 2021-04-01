
import glob
import sys
import numpy as np
import cv2

# Массив для хранения точек в 3d пространстве в мире (у доски в миреб найдем заранее)
points_3d = []
# Массив для хранения точек в 2d пространстве на изображении (доска на изображении с камеры)
points_2d = []

# Параметры шахматной доски
# Число внутренних пересечений квадратов:
WIDTH = 9
HEIGHT = 6
CHECKERBOARD = (WIDTH, HEIGHT)
# Размер квадрата
SQUARE_SIZE = 0.0247 #м


criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((WIDTH*HEIGHT, 3), np.float32)
objp[:,:2] = np.mgrid[0:WIDTH,0:HEIGHT].T.reshape(-1,2)
objp = objp * SQUARE_SIZE
# Критерии для остановки калибровки
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


img_paths = glob.glob('/home/pi/Documents/omni-platform-python/camera_calibration/img/*.jpeg')


for img_path in img_paths:
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if img is None:
        sys.exit("Could not read the image.")

    ret, corners = cv2.findChessboardCorners(img, CHECKERBOARD, None)

    list_of_digits = [int(s) for s in img_path if s.isdigit()]
    img_number = ''.join(str(i) for i in list_of_digits)
    print(f"{img_number}: {ret}")
    if ret:
        points_3d.append(objp)

        corners_sp = cv2.cornerSubPix(img, corners, (11, 11), (-1, -1), criteria)
        points_2d.append(corners_sp)

        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners_sp, ret)
        cv2.imshow(f"img {img_number}", img)
        cv2.waitKey(500)


ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(points_3d, points_2d, img.shape[::-1], None, None)

print("Camera matrix:")
print(mtx, "\n")
print("Dist:")
print(dist)

cv2.waitKey(1000)
cv2.destroyAllWindows()
# ------------------------ found camera params -----------------------------
# Camera matrix:
# [[498.09258835   0.         323.40423058]
#  [  0.         497.70636798 247.28028059]
#  [  0.           0.           1.        ]] 

# Dist:
# [[ 0.1956769  -0.49535501 -0.00098623  0.00081702  0.35487589]]