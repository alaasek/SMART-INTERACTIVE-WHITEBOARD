
import cv2
import numpy as np

def detect_red_marker(frame):
    """
    Detect red regions in the camera frame using HSV color filtering.
    Returns the detection mask and the center of the best candidate.
    """

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red can appear at both ends of the HSV hue range.
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 100, 50])
    upper_red2 = np.array([179, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = cv2.bitwise_or(mask1, mask2)

    # Remove small isolated noise.
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    candidates = [
        contour for contour in contours
        if cv2.contourArea(contour) > 20
    ]

    if not candidates:
        return mask, None

    # Initial prototype: choose the largest red candidate.
    best = max(candidates, key=cv2.contourArea)

    moments = cv2.moments(best)

    if moments["m00"] == 0:
        return mask, None

    center_x = int(moments["m10"] / moments["m00"])
    center_y = int(moments["m01"] / moments["m00"])

    return mask, (center_x, center_y)
