import numpy as np
import cv2

#synthetic camera scene

width = 640
height = 480

image = np.zeros((height,width),dtype=np.uint8)
print(image)

translation_center_x = 0
translation_center_y = 0
target_size = 1
target_point = int(5 * target_size)

# / output is float
# // output is floor , use // because we want to ues integer
cx = width // 2 + translation_center_x
cy = height // 2 + translation_center_y

box_w = int(128 * target_size)
box_h = int(192 * target_size)

#x1 y1 = upper left position
#x2 y2 = lower rifgt position
x1 = cx - box_w // 2
y1 = cy - box_h // 2
x2 = cx + box_w // 2
y2 = cy + box_h // 2

# print(x1)
# print(x2)
# print(y1)
# print(y2)

draw_target = cv2.rectangle(image, (x1,y1), (x2, y2), 255, 2)
target_image = cv2.circle(draw_target, (cx,cy), target_point, 255, 2)

print(cx)
print(cy)
cv2.imwrite('experiments/debug_images/target_medium.png', target_image)