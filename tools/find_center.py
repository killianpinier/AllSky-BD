import cv2 as cv

img_path = str(input("Calibrating image path (relative): "))

img = cv.imread(img_path)
assert img is not None, "Error: Image could not be read. Check path"

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_blur = cv.GaussianBlur(img_gray, (5, 5), 0)
_, threshold = cv.threshold(img_blur, 20, 255, cv.THRESH_BINARY)
contours, _ = cv.findContours(threshold, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

circle = [ct for ct in contours if cv.arcLength(ct, True) > 4000][0]

(x, y), radius = cv.minEnclosingCircle(circle)
center = (int(x), int(y))
radius = int(radius)

cv.circle(img, center, radius, (255, 0, 0), 10)
cv.circle(img, center, 50, (255, 0, 0), -1)
cv.circle(img, center, 20, (0, 0, 255), -1)
cv.putText(img, f"Center: ({center[0]}, {center[1]})", (img.shape[1]//20, img.shape[0]//16), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)

print(f"Center: ({center[0]}, {center[1]})")
cv.imwrite("camera_center.png", img)