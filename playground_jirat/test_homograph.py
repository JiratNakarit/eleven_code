import os
import sys
import numpy as np
import cv2
import sympy

# import module from folder sec
home_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
module_path = os.path.abspath(os.path.join(home_path, 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)

from camera import *
from helper_image import *


def dot_m():
    fx, fy, cx, cy = sympy.symbols('fx fy cx cy')
    r11, r12, r13 = sympy.symbols('r11 r12 r13')
    r21, r22, r23 = sympy.symbols('r21 r22 r23')
    r31, r32, r33 = sympy.symbols('r31 r32 r33')
    tx, ty, tz = sympy.symbols('tx ty tz')
    x, y, z = sympy.symbols('x y z')
    s, u, v = sympy.symbols('s u v')

    k = np.asanyarray([[fx, 0, cx],
                       [0, fy, cy],
                       [0, 0, 1]])

    image = np.asanyarray([[u],
                           [v],
                           [1]])

    world = np.asanyarray([[x],
                           [y],
                           [z],
                           [1]])

    Rt = np.asanyarray([[r11, r12, r13, tx],
                        [r21, r22, r23, ty],
                        [r31, r32, r33, tz]])
    r = np.dot(k, Rt)
    print(r)
    r = np.dot(r, world)
    print(r)


def get_extrinsic(u, v, M):

    m = np.asarray([[u[0]], [v[0]], [1],
                    [u[1]], [v[1]], [1],
                    [u[2]], [v[2]], [1],
                    [u[3]], [v[3]], [1]])

    A = np.loadtxt("array.txt", delimiter=',')
    fx = A[0][0]
    fy = A[1][1]
    cx = A[0][2]
    cy = A[1][2]

    print(fx, '||', fy, '||', cx, '||', cy)

    x = M[0]
    y = M[1]
    z = M[2]
    cof = [[x[0]*fx, y[0]*fx, z[0]*fx, 0, 0, 0, x[0]*cx, y[0]*cx, z[0]*cx, fx, 0, cx],
           [0, 0, 0, x[0]*fy, y[0]*fy, z[0]*fy, x[0]*cy, y[0]*cy, z[0]*cy, 0, fy, cy],
           [0, 0, 0, 0, 0, 0, x[0], y[0], z[0], 0, 0, 1],
           [x[1]*fx, y[1]*fx, z[1]*fx, 0, 0, 0, x[1]*cx, y[1]*cx, z[1]*cx, fx, 0, cx],
           [0, 0, 0, x[1]*fy, y[1]*fy, z[1]*fy, x[1]*cy, y[1]*cy, z[1]*cy, 0, fy, cy],
           [0, 0, 0, 0, 0, 0, x[1], y[1], z[1], 0, 0, 1],
           [x[0]*fx, y[2]*fx, z[2]*fx, 0, 0, 0, x[2]*cx, y[2]*cx, z[2]*cx, fx, 0, cx],
           [0, 0, 0, x[2]*fy, y[2]*fy, z[2]*fy, x[2]*cy, y[2]*cy, z[2]*cy, 0, fy, cy],
           [0, 0, 0, 0, 0, 0, x[2], y[2], z[2], 0, 0, 1],
           [x[0]*fx, y[3]*fx, z[3]*fx, 0, 0, 0, x[3]*cx, y[3]*cx, z[3]*cx, fx, 0, cx],
           [0, 0, 0, x[3]*fy, y[3]*fy, z[3]*fy, x[3]*cy, y[3]*cy, z[3]*cy, 0, fy, cy],
           [0, 0, 0, 0, 0, 0, x[3], y[3], z[3], 0, 0, 1]]

    T_cof = np.transpose(cof)
    # inv_cof = np.multiply(T_cof, np.linalg.inv(np.multiply(cof, T_cof)))

    print(cof)
    inv_cof = np.linalg.inv(cof)
    Rt = np.multiply(m, inv_cof)

    return Rt

cam = Camera(640, 30)

while True:
    depth_frame, color_frame = cam.get_frame()
    depth_img, color_img = cam.get_image(depth_frame, color_frame)
    # gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

    contour = get_contours(color_img)
    square, left, right, center = get_square(contour, 1000)

    cv2.drawContours(color_img, square, -1, (255,255,0), 3)

    M = [[-13.1, 3.2, -13.1, 3.2],
         [30.5, 30.5, 46.8, 46.8],
         [10, 10, 10, 10]]

    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k == ord('s'):
        u = []
        v = []
        for i in range(2):
            u.append(left[i][0])
            v.append(left[i][1])
            u.append(right[i][0])
            v.append(right[i][1])

            # print(v)
            # print(u)

        # extrinsic = get_extrinsic(u, v, M)
        dot_m()
    cv2.imshow('name', color_img)

