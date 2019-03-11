import os
import sys
import cv2
import glob
import time
import numpy as np

# import module from folder sec
home_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
module_path = os.path.abspath(os.path.join(home_path, 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)

from camera import *

camera = Camera()

counter = 1
side = ['front_', 'left_', 'right_']
light = ['sunny_', 'rainy_', 'cloudy_', 'indoor_']

for i in range(len(side)):
    print(str(i), ': ', side[i])
side_in = input('Select Side: ')
side_in = side[int(side_in)]

for i in range(len(light)):
    print(str(i), ': ', light[i])
light_in = input('Select Light Condition: ')
light_in = light[int(light_in)]

time_in = input('Time: ')

dist_in = input('Distance: ')

name = side_in + light_in + time_in + '_' + dist_in + '_'
print('File name: ', name)

time.sleep(1.5)
print('\n'*8)

while True:
    depth_frame, color_frame = camera.get_frame()
    depth_img, color_img = camera.get_image(depth_frame, color_frame)

    print(depth_frame.get_distance(320, 240))

    cv2.imshow("frame", color_img)
    cv2.imshow('ff', cv2.applyColorMap(cv2.convertScaleAbs(depth_img, alpha=0.0255), cv2.COLORMAP_JET))
    k = cv2.waitKey(1)
    if k == ord("q"):
        cv2.destroyAllWindows()
        camera.release_camera()
        break
    elif k == ord("s"):
        file_list = glob.glob('out\\rep_data\\*.jpg')
        # print(file_list)
        while True:
            path = 'out\\rep_data\\' + name + str(counter) + '.jpg'
            if path not in file_list:
                cv2.imwrite(path, color_img)

                print("save: " + path)
                break
            else:
                counter = counter + 1

