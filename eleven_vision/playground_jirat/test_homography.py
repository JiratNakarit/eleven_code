import os
import sys

# import module from folder sec
home_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
module_path = os.path.abspath(os.path.join(home_path, 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)

import numpy as np
import cv2
from camera import *
from helper_image import *


cam = Camera(640, 30)

state = 0

while True:
    depth_frame, color_frame = cam.get_frame()
    depth_img, color_img = cam.get_image(depth_frame, color_frame)

    contour = get_contours(color_img)
    square, left, right = get_square(contour, 1000)
    cv2.drawContours(color_img, square, -1, (255, 255, 0), 3)

    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k == ord('s'):
        if state == 0:
            pts_src = np.array(left + right)
            # pts_src = np.array(left[0])
            cv2.imwrite('out/im_src.jpg', color_img)
        elif state == 1:
            pts_dst = np.array(left + right)
            # pts_dst = np.array(left[0])
            cv2.imwrite('out/im_dst.jpg', color_img)
        state += 1

    if state >= 2:
        if state == 2:
            cv2.destroyAllWindows()
            im_src = cv2.imread('out/im_src.jpg')
            im_dst = cv2.imread('out/im_dst.jpg')
            h, status = cv2.findHomography(pts_src, pts_dst)
            im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))
        state += 1
        if state == 3:
            print(h)
        cv2.imshow("Warped Source Image", im_out)
    else:
        cv2.imshow('image', color_img)
