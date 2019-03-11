import os
import sys
import numpy as np
import cv2
from camera import *

class Calibration:

    def __init__(self):
        self.counter = 0
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.objp = np.zeros((9*7, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:7, 0:9].T.reshape(-1, 2)
        self.objpoints = [] # 3d point in real world space
        self.imgpoints = [] # 2d points in image plane.

    def find_chess(self, color_img):
        gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (7, 9), None)
        return ret, corners

    def append_objectpoint(self, ret, corners):
        if ret:
            self.objpoints.append(self.objp)
            self.imgpoints.append(corners)
