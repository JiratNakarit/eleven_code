import os
import sys
import math

# import module from folder sec
home_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
module_path = os.path.abspath(os.path.join(home_path, 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)

import numpy as np
import cv2
from camera import *
from helper_image import *


def SensorCoor(co_list):
    new_co = []
    for l in co_list:
        x = (l[0]-319)*3e-6
        y = (l[1]-239)*3e-6
        new_co.append([x, y])
    return new_co


def find_c(a, b):

    a = math.pow(a, 2)
    b = math.pow(b, 2)
    c = math.sqrt(a+b)
    return c


cam = Camera(640, 30)

state = 0
R1 = []
R2 = []

pts_src = np.asanyarray([[-80e-3, 80e-3], [-80e-3, -80e-3], [80e-3, 80e-3], [80e-3, -80e-3]])

while True:
    depth_frame, color_frame = cam.get_frame()
    depth_img, color_img = cam.get_image(depth_frame, color_frame)

    contour = get_contours(color_img)
    square, left, right, center = get_square(contour, 5000, 200000)
    cv2.drawContours(color_img, square, -1, (255, 255, 0), 3)
    cv2.circle(color_img, (319, 239), 2, (127, 0, 127))
    cv2.circle(color_img, tuple(center), 2, (127, 0, 255))

    k = cv2.waitKey(2)
    # print(k)
    if k == 27:
        break
    elif k == ord('s'):
        left = SensorCoor(left)
        right = SensorCoor(right)
        pts_dst = np.asanyarray(left + right)
        h, status = cv2.findHomography(pts_src, pts_dst)
        print('Homography Matrix:')
        print(h)
        print('')
        print('pts_src: ', pts_src)
        print('pts_dst: ', pts_dst)
    elif k == ord('a'):
        print(center)
        center = SensorCoor([center])[0]
        point = np.asanyarray([[center[0]], [center[1]], [1]])
        h = np.asanyarray(h)
        out = np.dot(np.linalg.inv(h), point)
        print(out)
    elif k == ord('d'):
        K = np.loadtxt("array.txt", delimiter=',')
        K = np.asanyarray(K)
        rt = np.dot(np.linalg.inv(K), h)

        for i in range(3):
            R1.append(rt[i][0])
            R2.append(rt[i][1])
        R1 = np.asanyarray(R1)
        R2 = np.asanyarray(R2)
        R3 = np.cross(R1, R2)
        print(R3)
        # print(R2)

        print(rt)
    cv2.imshow('img', color_img)
