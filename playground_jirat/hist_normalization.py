import cv2
import numpy as np
from matplotlib import pyplot as plt


image = cv2.imread('out/rep_data/front_cloudy_15_450_1.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)



cv2.imshow('Image', image)
cv2.waitKey(0)

