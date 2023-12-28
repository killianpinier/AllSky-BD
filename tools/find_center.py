"""
find_center.py

- Author: Killian Pinier
- Date: December 28, 2023
- Description: This small script uses OpenCv to determine the image center from a 
  picture taken with a large fov lens. For some reason, when a fisheye lens is put 
  on top of a raspberry pi camera chip, the center of the circle created is not 
  aligned with the center of the image.
- Instructions: In order to obtain the most precise center, place a homogeneous material
  that allows light to pass through it (e.g. a white shirt) and a source of white light
  on top of it.

"""

import cv2 as cv

img_path = str(input("Calibrating image path: "))

img = cv.imread(img_path)
assert img is not None, "Error: Image could not be read. Check path"

# Convert image to gray scale, and use Gaussian blurring to reduce noise.
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_blur = cv.GaussianBlur(img_gray, (5, 5), 0)

# Convert filtered image to binary format (black and white). 
# If instructions are followed correctly, 20 should a good threshold.
_, threshold = cv.threshold(img_blur, 20, 255, cv.THRESH_BINARY)
contours, _ = cv.findContours(threshold, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

# Filter countours with a larger perimeter than 0-axis size of the image (0-axis size is a resonable value)
filtered_countours = [ct for ct in contours if cv.arcLength(ct, True) > img.shape[0]]
(x, y), radius = (0, 0), 0

# Get the largest enclosing circle
for c in filtered_countours:
    (x, y), rad = cv.minEnclosingCircle(c)
    if rad > radius:
        center = (int(x), int(y))
        radius = int(rad)

# Draw the contour fit, and display the lens center
cv.circle(img, center, radius, (255, 0, 0), 10)
cv.circle(img, center, 50, (255, 0, 0), -1)
cv.circle(img, center, 20, (0, 0, 255), -1)
cv.putText(img, f"Center: ({center[0]}, {center[1]})", (img.shape[1]//20, img.shape[0]//16), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
cv.putText(img, f"Radius: {radius}", (img.shape[1]//20, img.shape[0]//16+120), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)

print(f"Center: ({center[0]}, {center[1]})")
print(f"Radius: {radius}")

cv.imwrite("camera_center.png", img)