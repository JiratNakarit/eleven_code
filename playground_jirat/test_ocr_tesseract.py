import os
import sys
import cv2
import glob
import numpy as np
import pytesseract
from PIL import Image
from matplotlib import pyplot as plt

home_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if home_path not in sys.path:
    sys.path.append(home_path)

from helper_image import *


def create_display(width, height, corners):
    block1_pst1 = np.float32(corners)
    block1_pst2 = np.float32([[0, 0], [0, height], [width, 0], [width, height]])
    transform = cv2.getPerspectiveTransform(block1_pst1, block1_pst2)
    warp_transform = cv2.warpPerspective(img, transform, (width, height))
    return warp_transform

home_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
dirs_path = os.path.abspath(os.path.join(home_path, 'get_data'))
data_path = os.path.abspath(os.path.join(dirs_path, 'data_rs'))

list_data_path = glob.glob(data_path + '\*.jpg')

sample_data_path = list_data_path[0]

img = cv2.imread(sample_data_path)

# --------------------------------------------------------------------------------------------------------------
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
contours = get_contours(img)
square, left, right, center = get_square(contours, 5000, 200000)

block1_corners = [left[0], left[2], right[0], right[2]]
block2_corners = [left[1], left[3], right[1], right[3]]

display_left = create_display(140, 254, block1_corners)
display_right = create_display(140, 254, block2_corners)

# cv2.drawContours(img, square, -1, (255, 255, 0), 2)
# cv2.circle(img, tuple(left[2]), 3, (255, 128, 128), 3)

# --------------------------------------------------------------------------------------------------------------

plt.subplot(121), plt.imshow(display_left), plt.title('display_left')
plt.subplot(122), plt.imshow(display_right), plt.title('display_right')
# plt.subplot(212), plt.imshow(img), plt.title('Image')
plt.show()

# --------------------------------------------------------------------------------------------------------------

txt = pytesseract.image_to_string(display_left)
