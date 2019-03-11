import cv2
import time
import numpy as np
from camera import *
from matplotlib import pyplot as plt


rs = Camera(640, 15)

state = 0

while True:

    depth_frame, color_frame = rs.get_frame()
    depth_img, color_img = rs.get_image(depth_frame, color_frame)

    epoch = time.time()
    lt = time.localtime(epoch)

    print(lt.tm_min, '||', lt.tm_sec)

    if lt.tm_hour >= 0:
        if ((lt.tm_sec % 20) == 0) and (state != 1):
            state = 1
            file_name = "data_epoch/" + str(lt.tm_hour) + str(lt.tm_min) + str(lt.tm_sec) + ".jpg"
            cv2.imwrite(file_name, color_img)
            print('save')
        if ((lt.tm_sec % 20) != 0) and (state == 1):
            state = 0
    if lt.tm_hour == 19 and lt.tm_min != 0:
        break

cv2.destroyAllWindows()
rs.release_camera()
