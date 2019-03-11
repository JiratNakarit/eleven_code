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
from helper_image import *


# define some constance
i = 0
FocalLength = 1.93e-3
box_left = []
box_right = []
intrinsic = np.loadtxt("playground_jirat/array.txt", delimiter=',')


# import picture
home_path = os.path.dirname(os.path.realpath(__file__))
playground_path = os.path.abspath(os.path.join(home_path, 'playground_jirat'))
out_path = os.path.abspath(os.path.join(playground_path, 'out'))
picture_path = os.path.abspath(os.path.join(out_path, 'rep_data'))
list_data = glob.glob(picture_path + '/*.jpg')


def img_to_sensor(co_list):
    new_co = []
    for l in co_list:
        print('old: ', l)
        x = (l[0])*3e-6
        y = (l[1])*3e-6
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


def tz_from_rs(point, depth_frame):
    if type(point) == list:
        distance = depth_frame.get_distance(point[0], point[1])
        return distance
    else:
        distance = []
        for pnt in point:
            dst = depth_frame.get_distance(pnt[0], pnt[1])
            distance.append(dst)
        return distance


while True:

    try:
        image = cv2.imread(list_data[i])
    except:
        print('End of series')
        break

    contours = get_contours(image)
    square, left, right, center = get_square(contours, 5000, 200000)

    number_of_contours = len(center)

    if number_of_contours == 2:
        box_left.append(left[0])
        box_left.append(left[2])
        box_right.append(right[0])
        box_right.append(right[2])

    # cv2.drawContours(image, square, -1, (255, 255, 0), 2)
    # draw_contours(image, box_left, box_right)

    point_center_x = int((center[0][0] + center[1][0]) / 2)
    point_center_y = int((center[0][1] + center[1][1]) / 2)
    point_center = (point_center_x, point_center_y)
    picture_center = (320, 240)

    if point_center_x <= picture_center[0]:
        delta_x = find_euclidean(list(picture_center), [point_center_x, picture_center[1]]) * -1
    else:
        delta_x = find_euclidean(list(picture_center), [point_center_x, picture_center[1]])
    if point_center_y >= picture_center[1]:
        delta_y = find_euclidean(list(point_center), [point_center[0], picture_center[1]]) * -1
    else:
        delta_y = find_euclidean(list(point_center), [point_center[0], picture_center[1]])

    img_on_sensor = img_to_sensor([[delta_x, delta_y]])
    delta_x = img_on_sensor[0][0]
    delta_y = img_on_sensor[0][1]

    Z = 0.3
    X = (delta_x * Z) / FocalLength
    Y = (delta_y * Z) / FocalLength

    print('(', X, ',', Y, ',', Z, ')')

    cv2.line(image, picture_center, (point_center_x, picture_center[1]), (127, 255, 0), 1)
    cv2.line(image, point_center, (point_center[0], picture_center[1]), (127, 255, 0), 1)
    cv2.circle(image, point_center, 3, (0, 0, 255))
    cv2.circle(image, picture_center, 3, (255, 0, 0))

    cv2.putText(image, 'X:', (5, 410), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))
    cv2.putText(image, format(X, '.3f'), (35, 410), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))
    cv2.putText(image, 'Y:', (5, 440), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))
    cv2.putText(image, format(Y, '.3f'), (35, 440), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))
    cv2.putText(image, 'Z:', (5, 470), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))
    cv2.putText(image, format(Z, '.3f'), (35, 470), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))

    cv2.imshow('Image', image)
    k = cv2.waitKey(0)

    if k == 27:
        break
    elif k == ord('c'):
        cv2.destroyAllWindows()
        i += 1

cv2.destroyAllWindows()



