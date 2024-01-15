"""
reshape_img.py

- Author: Killian Pinier
- Date: January 15, 2023
- Description: This script uses OpenCv to reshape an image containing a circle so that 
  its center matches with the one of the image. The resulting image is a square with
  dimensions equal to the diameter of the circle.

"""

import cv2
import numpy as np

def recenter_image(img, center, radius):
    # Move the circle to the top-left edges of the image 
    x_shift = radius - center[0]
    y_shift = radius - center[1]
    M = np.float32([[1, 0, x_shift], [0, 1, y_shift]])
    # Apply translation, and reshape image to a square with sides equal to the diameter of the circle
    shifted_img = cv2.warpAffine(img, M, (radius*2, radius*2))
    return shifted_img

img_path = str(input("Image path: "))
x_center = int(input("X center: "))
y_center = int(input("Y center: "))
radius   = int(input("Radius: "))

img = cv2.imread(img_path)
recentered_img = recenter_image(img, (x_center, y_center), radius)
cv2.imwrite("formatted_img.png", recentered_img)

