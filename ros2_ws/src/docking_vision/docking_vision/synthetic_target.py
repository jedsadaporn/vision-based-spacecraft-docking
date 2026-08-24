import numpy as np
import cv2

#synthetic camera scene

class SpacecraftState:
    def __init__(self, x, y, z):
        self.x = x       # lateral position
        self.y = y       # vertical position
        self.z = z       # distance to docking target

def create_target(image, state):
    width = 640
    height = 480

    translation_center_x = state.x
    translation_center_y = state.y
    distance = state.z

    target_point = max(1, int(5 / distance))

    cx = int(width // 2 + translation_center_x)
    cy = int(height // 2 + translation_center_y)

    box_w = int(128 / distance)
    box_h = int(192 / distance)
    # print("box_w", box_w)
    # print("box_h", box_h)

    x1 = int(cx - box_w // 2)
    y1 = int(cy - box_h // 2)
    x2 = int(cx + box_w // 2)
    y2 = int(cy + box_h // 2)

    draw_target = cv2.rectangle(image, (x1,y1), (x2, y2), 255, 2)
    target_image = cv2.circle(draw_target, (cx,cy), target_point, 255, 2)

    return target_image