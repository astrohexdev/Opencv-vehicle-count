import cv2
import time
import numpy as np
from utils import center_position, RED, GREEN, BLUE, ORANGE, FONT

def bg_sub(show_detect, show_subtract, CAP, fps=60, linePos=550, min_width=80, min_height=80, offset=6):
    subtract = cv2.createBackgroundSubtractorMOG2()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    detect_vehicle = []
    counts = 0

    cv2.namedWindow('Detect', cv2.WINDOW_NORMAL)
    if show_detect.startswith('y'):
        cv2.namedWindow('Detector', cv2.WINDOW_NORMAL)
    if show_subtract.startswith('y'):
        cv2.namedWindow('Subtracted', cv2.WINDOW_NORMAL)

    while CAP.isOpened():
        time.sleep(1 / fps)

        ret, frame = CAP.read()
        if not ret or frame is None:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 5)

        img_sub = subtract.apply(blur)
        dilation = cv2.dilate(img_sub, np.ones((5, 5)))
        opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
        contours = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

        cv2.line(frame, (25, linePos), (1200, linePos), BLUE, 2)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w >= min_width and h >= min_height:
                cv2.rectangle(frame, (x, y), (x + w, y + h), GREEN, 2)
                center_vehicle = center_position(x, y, w, h)
                detect_vehicle.append(center_vehicle)
                cv2.circle(frame, center_vehicle, 4, RED, -1)

                for cx, cy in detect_vehicle:
                    if linePos - offset < cy < linePos + offset:
                        cv2.line(frame, (25, linePos), (1200, linePos), ORANGE, 3)
                        detect_vehicle.remove((cx, cy))
                        counts += 1

        cv2.putText(frame, f"Car Detected: {counts}", (50, 70), FONT, 2, RED, 3, cv2.LINE_AA)
        cv2.imshow('Detect', frame)

        if show_detect.startswith('y'):
            cv2.imshow('Detector', opening)
        if show_subtract.startswith('y'):
            cv2.imshow('Subtracted', img_sub)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cv2.destroyAllWindows()
    CAP.release()
    return counts
