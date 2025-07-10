import cv2

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (176, 130, 39)
ORANGE = (0, 127, 255)

FONT = cv2.FONT_HERSHEY_COMPLEX

def center_position(x, y, w, h):
    center_x = x + (w // 2)
    center_y = y + (h // 2)
    return center_x, center_y
