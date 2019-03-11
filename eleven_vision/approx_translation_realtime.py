import cv2
import math
import numpy as np
from camera import *
from helper_image import *


# define some constance
i = 0
box_left = []
box_right = []
intrinsic = np.loadtxt("playground_jirat/array.txt", delimiter=',')


# define realsense
camera = Camera(640, 30)
FocalLength = 1.93e-3  # meters


def img_to_sensor(coordinate_list):
    new_coordinate = []
    for l in coordinate_list:
        x = (l[0])*3e-6  # meters
        y = (l[1])*3e-6  # meters
        new_coordinate.append([x, y])
    return new_coordinate


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


class Translation:

    def __init__(self, depth_frame, color_image, center):
        self.depth_frame = depth_frame
        self.color_image = color_image
        self.center = center
        x, y, z = self.get_xy()
        self.x = x
        self.y = y
        self.z = z

    def tz_from_rs(self, point):
        if type(point) == list:
            distance = []
            for pnt in point:
                dst = self.depth_frame.get_distance(pnt[0], pnt[1])
                distance.append(dst)
            return distance
        else:
            distance = self.depth_frame.get_distance(point[0], point[1])
            return distance

    def get_z(self, point_center):
        Z = self.tz_from_rs(point_center)
        return Z

    def get_xy(self):
        point_center_x = int((center[0][0] + center[1][0]) / 2)
        point_center_y = int((center[0][1] + center[1][1]) / 2)
        point_center = (point_center_x, point_center_y)
        picture_center = (320, 240)
        delta_x = find_euclidean(list(picture_center), [point_center_x, picture_center[1]])
        delta_y = find_euclidean(list(point_center), [point_center[0], picture_center[1]])
        img_on_sensor = img_to_sensor([[delta_x, delta_y]])
        delta_x = img_on_sensor[0][0]
        delta_y = img_on_sensor[0][1]
        Z = self.tz_from_rs(point_center)
        X = (delta_x * Z) / FocalLength
        Y = (delta_y * Z) / FocalLength
        return X, Y, Z


if __name__ == '__main__':

    while True:
        depth_frame, color_frame = camera.get_frame()
        depth_img, color_img = camera.get_image(depth_frame, color_frame)

        contours = get_contours(color_img)
        square, left, right, center = get_square(contours, 5000, 200000)

        number_of_contours = len(center)

        cv2.drawContours(color_img, square, -1, (255, 255, 0), 2)

        if number_of_contours == 2:
            trans = Translation(depth_frame, color_img, center)

            print(trans.x)

        # cv2.line(color_img, picture_center, (point_center_x, picture_center[1]), (127, 255, 0), 1)
        # cv2.line(color_img, point_center, (point_center[0], picture_center[1]), (127, 255, 0), 1)
        #
        # cv2.circle(color_img, point_center, 3, (0, 0, 255))
        # cv2.circle(color_img, picture_center, 3, (255, 0, 0))

            cv2.putText(color_img, 'X:', (5, 410), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))
            cv2.putText(color_img, format(trans.x, '.3f'), (35, 410), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))
            cv2.putText(color_img, 'Y:', (5, 440), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))
            cv2.putText(color_img, format(trans.y, '.3f'), (35, 440), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))
            cv2.putText(color_img, 'Z:', (5, 470), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))
            cv2.putText(color_img, format(trans.z, '.3f'), (35, 470), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))

        cv2.imshow('Image', color_img)
        k = cv2.waitKey(1)

        if k == 27:
            break

    cv2.destroyAllWindows()




