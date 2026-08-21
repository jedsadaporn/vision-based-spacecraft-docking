import numpy as np
import cv2

# image = cv2.imread('target_medium.png')
image = cv2.imread('target_medium.png',cv2.IMREAD_GRAYSCALE)

threshold = 120

print(image.shape)
print(image.dtype)
print(image.size)

print(image[240, 320])
print(image[240, 315])
print(image[240, 314])

#threshold pixel < threshold -> 0 , Background 
#threshold pixel >= threshold -> 1 , Target
#cv2.THRESH_BINARY , Above threshold -> 255, below -> 0.
threshold_value, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
print(threshold_value)
print(binary_image)
print(binary_image.shape)
print(binary_image.dtype)
print(binary_image[240, 320])

# RETR_LIST
# cv2.RETR_EXTERNAL
contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.imshow('Binary Image', binary_image)

# print("Number of Contours Found = " + str(len(contours)))

for i, contour in enumerate(contours):
    print("Contour:", i)
    print("Number of points:", len(contour))

# cv2.imwrite('binary.png', binary_image)
# cv2.imshow("thresold image", thresold_image)

cv2.waitKey(0)
cv2.destroyAllWindows()