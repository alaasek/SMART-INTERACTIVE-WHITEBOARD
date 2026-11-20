
import cv2
import numpy as np

# 1. Board corners selected during calibration
source_points = np.float32([
    [111, 102],
    [480, 111],
    [497, 332],
    [123, 335]
])

# 2. Virtual board dimensions
width = 800
height = 450

# 3. Destination rectangle
destination_points = np.float32([
    [0, 0],
    [width, 0],
    [width, height],
    [0, height]
])

# 4. Calculate homography matrix
matrix = cv2.getPerspectiveTransform(
    source_points,
    destination_points
)


# 5. Map a camera point to the virtual board
def map_point(x, y):

    point = np.float32([[[x, y]]])

    transformed = cv2.perspectiveTransform(
        point,
        matrix
    )

    mapped_x = int(round(transformed[0][0][0]))
    mapped_y = int(round(transformed[0][0][1]))

    # Check if the point is inside the board
    if 0 <= mapped_x < width and 0 <= mapped_y < height:
        return mapped_x, mapped_y

    return None
