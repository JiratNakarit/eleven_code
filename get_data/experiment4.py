import os
import sys
import glob
import random as rd

home_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if home_path not in sys.path:
    sys.path.append(home_path)

from helper_image import *


index = []
samples = []
iteration = 1500

count = 0
positive_box = 0
negative_box = 0
negative_list = []

data = glob.glob('data_rs/*.jpg')

number_of_data = len(data)

for i in range(iteration):
    while True:
        i_index = rd.randint(0, number_of_data-1)
        if i_index not in index:
            index.append(i_index)
            samples.append(data[i_index])
            break

for path_img in samples:

    count += 1

    img = cv2.imread(path_img)

    contours = get_contours(img)
    square, left, right, center = get_square(contours, 5000, 200000)

    number_of_contours = len(center)

    cv2.drawContours(img, square, -1, (255, 255, 0), 2)

    if number_of_contours == 2:
        positive_box += 1
    else:
        negative_box += 1
        print(path_img)
        cv2.imwrite("out_fail/" + str(negative_box) + ".jpg", img)

    cv2.imshow('image', img)
    cv2.waitKey(50)
    cv2.destroyAllWindows()

print('pos: ', positive_box, ' || neg: ', negative_box)
print(count)
