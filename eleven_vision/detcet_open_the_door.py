import os
import sys
import cv2
import math
import glob
import numpy as np

# import module from folder sec
home_path = os.path.dirname(os.path.realpath(__file__))
module_path = os.path.abspath(os.path.join(home_path, 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)


from camera import *

camera = Camera(640, 30)

check_points = []
counter_lr = 0


def open_the_door(left_points, right_points, center_point):
    left_side = []
    right_side = []

    for left_pnt in left_points:
        if center_point - left_pnt >= 0.2:
            left_side.append(True)
        else:
            left_side.append(False)

    for right_pnt in right_points:
        if right_pnt - center_point >= 0.2:
            right_side.append(True)
        else:
            right_side.append(False)


while True:
    depth_frame, color_frame = camera.get_frame()
    depth_img, color_img = camera.get_image(depth_frame, color_frame)

    width = color_img.shape[1]
    height = color_img.shape[0]

    points_x = [int((0.5/8)*width), int((1/8)*width), int((7/8)*width), int((7.5/8)*width)]
    points_y = [int((2/8)*height), int((3/8)*height), int((4/8)*height), int((5/8)*height), int((6/8)*height)]

    for point_x in points_x:
        for point_y in points_y:
            check_points.append((point_x, point_y))
        counter_lr += 1

    for pnt in check_points:
        cv2.circle(color_img, pnt, 2, (0, 0, 255), 2)

    k = cv2.waitKey(1)
    if k == 27:
        break

    cv2.imshow('color_image', color_img)

cv2.destroyAllWindows()
camera.release_camera()
