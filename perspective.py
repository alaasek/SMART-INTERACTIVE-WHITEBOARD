
import cv2
import numpy as np

# Four corners selected during calibration
source_points = np.float32([
    [111, 102],
    [480, 111],
    [497, 332],
    [123, 335]
])

# Dimensions of the virtual board
width = 800
height = 450

# Destination rectangle
destination_points = np.float32([
    [0, 0],
    [width, 0],
    [width, height],
    [0, height]
])

# Calculate perspective transformation
matrix = cv2.getPerspectiveTransform(
    source_points,
    destination_points
)

# Open camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)
    # Draw the selected board corners
    for point in source_points.astype(int):
        cv2.circle(frame, tuple(point), 7, (0, 255, 0), -1)

    # Connect the four corners
    cv2.polylines(
        frame,
        [source_points.astype(int)],
        True,
        (0, 255, 0),
        2
    )

    # Apply perspective transformation
    warped = cv2.warpPerspective(
        frame,
        matrix,
        (width, height)
    )

    cv2.imshow("Original Camera", frame)
    cv2.imshow("Virtual Board", warped)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
