import numpy as np
import cv2


def break_background(frame, lower, upper):
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(frame, lower, upper)
    output = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('mask', output)


def get_contours(frame):
    kernel = np.ones((2, 2), np.uint8)

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
    # threshold = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 7)
    # edges = cv2.Canny(threshold,200,300)
    # threshold2 = cv2.threshold(img_gray, 60, 255, cv2.THRESH_BINARY)[1]
    # img_cont, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    edges = cv2.Canny(img_gray, 100, 20)
    edges = cv2.dilate(edges, kernel, iterations=1)
    ret, contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.imshow('img_gray', img_gray)
    cv2.imshow('edges', edges)
    # cv2.imshow('threshold', threshold)
    # cv2.imshow('threshold2', threshold2)
    return contours


def get_square(contours, area_lower, area_upper):
    selected_contours = []
    new_approx = []

    cx = 0
    cy = 0

    center = []
    left_side = []
    right_side = []
    new_left_side = []
    new_right_side = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if (area <= area_upper) and (area > area_lower):
            # print(cv2.contourArea(cnt))
            epsilon = 0.1 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            if len(approx) == 4:
                selected_contours.append(cnt)

                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                center.append([cx, cy])
                for i in approx:
                    new_approx.append(i[0])
                old_coor = sorted(new_approx, key=lambda k: [k[0], k[1]])
                left_side.append(old_coor[0])
                left_side.append(old_coor[1])
                right_side.append(old_coor[2])
                right_side.append(old_coor[3])
                new_left_side = sorted(left_side, key=lambda k: [k[1], k[0]])
                new_right_side = sorted(right_side, key=lambda k: [k[1], k[0]])

    return selected_contours, new_left_side, new_right_side, center


def normalized_hist(frame):

    pass


if __name__ == "__main__":

    from camera import *

    rs = Camera()

    while True:
        depth_frame, color_frame = rs.get_frame()
        depth_img, color_img = rs.get_image(depth_frame, color_frame)

        cv2.imshow('Image', color_img)
        cv2.waitKey(0)
