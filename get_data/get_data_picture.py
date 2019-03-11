import cv2
import numpy as np
from camera import *
from matplotlib import pyplot as plt


rs = Camera(640, 15)
bgst_mog = cv2.bgsegm.createBackgroundSubtractorMOG()
# bgst_mog2 = cv2.createBackgroundSubtractorMOG2()
bgst_gmg = cv2.bgsegm.createBackgroundSubtractorGMG()
kernel_gmg = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

while True:

    depth_frame, color_frame = rs.get_frame()
    depth_img, color_img = rs.get_image(depth_frame, color_frame)

    fgmask_mog = bgst_mog.apply(color_img)
    fgmask_gmg = bgst_gmg.apply(color_img)
    fgmask_gmg = cv2.morphologyEx(fgmask_gmg, cv2.MORPH_OPEN, kernel_gmg)

    hist1 = cv2.calcHist([fgmask_mog], [0], None, [256], [0, 255])
    hist2 = cv2.calcHist([fgmask_gmg], [0], None, [256], [0, 255])

    img1 = np.hstack((fgmask_mog, fgmask_gmg))
    img2 = np.hstack((color_img, color_img))

    print(hist1[0][0], ' || ', hist2[0][0])
    # for i in range(len(hist)):
    #     if hist[i][0] != 0:
    #         print(i)

    cv2.imshow('IMG1', img1)
    cv2.imshow('IMG2', img2)
    k = cv2.waitKey(1)
    if k == 27:
        break

cv2.destroyAllWindows()
rs.release_camera()
