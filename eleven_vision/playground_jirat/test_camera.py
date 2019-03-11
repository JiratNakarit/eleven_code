import os
import sys
import math
import numpy as np
import cv2
import pandas as pd

# import module from folder sec
home_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
module_path = os.path.abspath(os.path.join(home_path, 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)

from camera import *
from helper_image import *


def img_to_sensor(co_list):
    new_co = []
    for l in co_list:
        x = (l[0]-319)*3e-6
        y = (l[1]-239)*3e-6
        new_co.append([x, y])
    return new_co


def find_euclidean(point1, point2):
    if type(point1) == list:
        x1 = point1[0]
        y1 = point1[1]
        x2 = point2[0]
        y2 = point2[1]
        d = math.sqrt(math.pow((x1-x2), 2) + math.pow((y1-y2), 2))
        return d
    else:
        a = math.pow(point1, 2)
        b = math.pow(point2, 2)
        c = math.sqrt(a+b)
        return c


def tz_from_camera_madel(point1, point2):
    K = np.loadtxt("array.txt", delimiter=',')
    x = np.array([[find_euclidean(point1, point2)],
                  [0],
                  [0]])

    X = np.array([[abs(pts_src[0][0] - pts_src[2][0])],
                  [abs(pts_src[0][1] - pts_src[2][1])],
                  [0]])

    right_eq = np.dot(K, X)

    Tz = right_eq[0][0]/x[0][0]

    return Tz

cam = Camera(640, 30)
pts_src = [[-80e-3, 80e-3], [-80e-3, -80e-3], [80e-3, 80e-3], [80e-3, -80e-3]]

round = 0
distance = 0
FocalLength = 1.93



list_data = [0.3, 0.35, 0.4, 0.45, 0.6, 1.0, 1.4]

data = [[[], [], []],
        [[], [], []],
        [[], [], []],
        [[], [], []],
        [[], [], []],
        [[], [], []],
        [[], [], []],]

while True:
    depth_frame, color_frame = cam.get_frame()
    depth_img, color_img = cam.get_image(depth_frame, color_frame)

    contour = get_contours(color_img)
    square, left, right, center = get_square(contour, 5000, 200000)

    center_pix_top = (int(color_img.shape[1]/2), 0)
    center_pix_bot = (int(color_img.shape[1]/2), color_img.shape[0])
    center_pix_lef = (0, int(color_img.shape[0]/2))
    center_pix_rig = (color_img.shape[1], int(color_img.shape[0]/2))
    cv2.line(color_img, center_pix_top, center_pix_bot, (255, 0, 0), 2)
    cv2.line(color_img, center_pix_lef, center_pix_rig, (255, 0, 0), 2)

    try:
        center_top = (int((left[0][0]+right[0][0])/2), int((left[0][1]+right[0][1])/2))
        center_bot = (int((left[1][0]+right[1][0])/2), int((left[1][1]+right[1][1])/2))
        center_lef = (int((left[0][0]+left[1][0])/2), int((left[0][1]+left[1][1])/2))
        center_rig = (int((right[0][0]+right[1][0])/2), int((right[0][1]+right[1][1])/2))
        cv2.line(color_img, center_top, center_bot, (127, 0, 255), 2)
        cv2.line(color_img, center_lef, center_rig, (127, 0, 255), 2)
        cv2.circle(color_img, tuple(center), 2, (127, 0, 255))
        cv2.drawContours(color_img, square, -1, (127, 0, 255), 3)
    except:
        pass


    cv2.circle(color_img, (319, 239), 2, (127, 0, 127))


    k = cv2.waitKey(2)

    if k == 27:
        cam.release_camera()
        break
    elif k == ord('s'):
        left_sensor = img_to_sensor(left)
        D = find_euclidean(pts_src[0], pts_src[1])
        d = find_euclidean(left_sensor[0], left_sensor[1])

        perpen_d = find_euclidean(d/2, FocalLength)
        perpen_D = perpen_d*D/d

        Tz_similar_triangle = math.sqrt(math.pow(perpen_D, 2) - math.pow(D/2, 2))
        Tz_depth_realsenseD = depth_frame.get_distance(center[0], center[1])
        Tz_camera_model_cli = tz_from_camera_madel(left[0].tolist(), right[0].tolist())

        if round < 7:
            print('Experiment: ', round+1)
            if distance < 7:
                print('Distance @: ', list_data[distance])
                data[distance][0].append(Tz_similar_triangle)
                data[distance][1].append(Tz_depth_realsenseD)
                data[distance][2].append(Tz_camera_model_cli)
                distance = distance + 1

                print('Tz_similar_triangle', Tz_similar_triangle)
                print('Tz_depth_realsenseD', Tz_depth_realsenseD)
                print('Tz_camera_model_cli', Tz_camera_model_cli)
                print('\n'*2)

            if distance == 7:
                distance = 0
                round = round + 1

    if round == 7:
        print('End the process')

        data_similar_triangle = {'0.30': data[0][0],
                                     '0.35': data[1][0],
                                     '0.40': data[2][0],
                                     '0.45': data[3][0],
                                     '0.60': data[4][0],
                                     '1.00': data[5][0],
                                     '1.40': data[6][0]}

        data_depth_realsenseD = {'0.30': data[0][1],
                                     '0.35': data[1][1],
                                     '0.40': data[2][1],
                                     '0.45': data[3][1],
                                     '0.60': data[4][1],
                                     '1.00': data[5][1],
                                     '1.40': data[6][1]}

        data_camera_model_cli = {'0.30': data[0][2],
                                     '0.35': data[1][2],
                                     '0.40': data[2][2],
                                     '0.45': data[3][2],
                                     '0.60': data[4][2],
                                     '1.00': data[5][2],
                                     '1.40': data[6][2]}

        df_similar_triangle = pd.DataFrame(data=data_similar_triangle)
        df_depth_realsenseD = pd.DataFrame(data=data_depth_realsenseD)
        df_camera_model_cli = pd.DataFrame(data=data_camera_model_cli)

        df_similar_triangle.to_csv('out/data_similar_triangle.csv')
        df_depth_realsenseD.to_csv('out/data_depth_realsenseD.csv')
        df_camera_model_cli.to_csv('out/data_camera_model_cli.csv')

        print('Save')
        break

    cv2.imshow('img', color_img)
