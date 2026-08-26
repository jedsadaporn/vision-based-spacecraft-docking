import numpy as np
import cv2

def detect_target(image):
    threshold = 120
    print(image.shape)
    print(image.dtype)
    print(image)

    threshold_value, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for i, contour in enumerate(contours):
        print("Contour:", i)
        print("Number of points:", len(contour))

    x1, y1, box_w, box_h = cv2.boundingRect(contour)
    print(x1)
    print(y1)
    print(box_w)
    print(box_h)

    cx = x1 + box_w // 2
    cy = y1 + box_h // 2
    print('cx = ', cx)
    print('cy = ', cy)

    error_x = cx - 320
    error_y = cy - 240
    print('error x = ', error_x)
    print('error y = ', error_y)

    x2 = x1 + box_w
    y2 = y1 + box_h
    print(x2)
    print(y2)

    z_from_width = box_w / 128
    z_from_height = box_h / 192

    return cx, cy, z_from_width


# image = cv2.imread('target_medium.png')
image = cv2.imread('target_near.png',cv2.IMREAD_GRAYSCALE)
cx, cy, z_from_width = detect_target(image)
print("Target:", cx, cy, z_from_width)
# image = cv2.imread('target_right.png',cv2.IMREAD_GRAYSCALE)
# threshold = 120

# print(image.shape)
# print(image.dtype)
# print(image.size)

# print(image[240, 320])
# print(image[240, 315])
# print(image[240, 314])

#threshold pixel < threshold -> 0 , Background 
#threshold pixel >= threshold -> 1 , Target
#cv2.THRESH_BINARY , Above threshold -> 255, below -> 0.
# threshold_value, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
# print(threshold_value)
# print(binary_image)
# print(binary_image.shape)
# print(binary_image.dtype)
# print(binary_image[240, 320])

# RETR_LIST
# cv2.RETR_EXTERNAL
# Find the Contours
# contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# print("Number of Contours Found = " + str(len(contours)))

# for i, contour in enumerate(contours):
#     print("Contour:", i)
#     print("Number of points:", len(contour))

#Find Position by Contour
#x is x in upper left = x1 , y is y in upper left = y1
# x1, y1, box_w, box_h = cv2.boundingRect(contour)
# print(x1)
# print(y1)
# print(box_w)
# print(box_h)

#We know x1 , y1 , box_h, box_w
#We can find cx, 
#Find the cx position and cy position = x1 + box_w = x2 , so we can find the center by divide 2
# cx = x1 + box_w // 2
# cy = y1 + box_h // 2
# print('cx = ', cx)
# print('cy = ', cy)


# Target center = (cx, cy)
# Camera center = (320, 240)
# error_x = cx - 320
# error_y = cy - 240
# print('error x = ', error_x)
# print('error y = ', error_y)

#find the x2, y2 the lower right position
# x2 = x1 + box_w
# y2 = y1 + box_h
# print(x1)
# print(x2)

# draw_target = cv2.rectangle(binary_image, (x1,y1), (x2, y2), 255, 3)
# target_image = cv2.circle(draw_target, (cx,cy), 1, 255, 2)

# cv2.imwrite('target_from_contours.png', target_image)

# cv2.imshow('Binary Image', binary_image)
# cv2.imwrite('binary.png', binary_image)
# cv2.imshow("thresold image", thresold_image)

# cv2.waitKey(0)
# cv2.destroyAllWindows()