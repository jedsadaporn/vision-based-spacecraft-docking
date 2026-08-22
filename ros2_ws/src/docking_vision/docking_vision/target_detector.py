import numpy as np
import cv2

def detect_target(image):
    threshold = 120
    # print(image.shape)
    # print(image.dtype)
    # print(image)

    threshold_value, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for i, contour in enumerate(contours):
        print("Contour:", i)
        print("Number of points:", len(contour))

    print("min:", image.min())
    print("max:", image.max())
    print("unique:", np.unique(image))

    if len(contours) == 0:
        print("No contour found")
        return

    x1, y1, box_w, box_h = cv2.boundingRect(contour)
    # print(x1)
    # print(y1)
    # print(box_w)
    # print(box_h)

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
    # print(x2)
    # print(y2)



    return cx, cy
