
import cv2
import numpy as np
import time

from input_RedMarker.marker_detection import detect_red_marker
from coordinate_mapping import map_point, width, height
from interface import (
    draw_menu,
    get_hovered_button,
    draw_pen_settings,
    get_hovered_pen_option
)

SMOOTHING = 0.35
previous_point = None
smooth_point = None
# Virtual whiteboard
canvas = np.zeros((height, width, 3), dtype=np.uint8)

cap = cv2.VideoCapture(0)


DWELL_TIME = 1.0

current_hover = None
hover_start = None
activated_button = None
active_mode = "DRAW"

show_pen_settings = False

# Pen configuration
pen_color = (0, 0, 255)  # Red
pen_thickness = 4


current_pen_hover = None
pen_hover_start = None
activated_pen_option = None

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Keep the same orientation as calibration.
    frame = cv2.flip(frame, 1)

    mask, center = detect_red_marker(frame)

    board = np.zeros((height, width, 3), dtype=np.uint8)
    draw_menu(board)
    if show_pen_settings:
        draw_pen_settings(board)

    if center is not None:
        board_point = map_point(center[0], center[1])


        if board_point is not None:
            x, y = board_point

            if smooth_point is None:
                smooth_point = (x, y)
            else:
                smooth_x = int(SMOOTHING * x + (1 - SMOOTHING) * smooth_point[0])
                smooth_y = int(SMOOTHING * y + (1 - SMOOTHING) * smooth_point[1])
                smooth_point = (smooth_x, smooth_y)
            hovered_button = get_hovered_button(board_point)

            if hovered_button != current_hover:
                current_hover = hovered_button
                hover_start = time.time() if hovered_button is not None else None
                activated_button = None

            if hovered_button is not None and activated_button is None:
                elapsed = time.time() - hover_start

                if elapsed >= DWELL_TIME:
                    print("SELECTED:", hovered_button)

                    if hovered_button == "DRAW":
                        active_mode = "DRAW"

                    elif hovered_button == "ERASER":
                        active_mode = "ERASER"

                    elif hovered_button == "CLEAR BOARD":
                        canvas[:] = 0
                        previous_point = None
                        smooth_point = None

                    elif hovered_button == "PEN SETTINGS":
                        show_pen_settings = True

                    activated_button = hovered_button
            cv2.circle(board, smooth_point, 8, (0, 255, 0), 2)
            # Pen settings submenu interaction
            pen_option = None

            if show_pen_settings:
                pen_option = get_hovered_pen_option(board_point)

            if pen_option != current_pen_hover:
                current_pen_hover = pen_option
                pen_hover_start = time.time() if pen_option is not None else None
                activated_pen_option = None

            if pen_option is not None and activated_pen_option is None:
                elapsed = time.time() - pen_hover_start

                if elapsed >= DWELL_TIME:

                    if pen_option == "RED":
                        pen_color = (0, 0, 255)
                        print("Pen color: RED")

                    elif pen_option == "BLUE":
                        pen_color = (255, 0, 0)
                        print("Pen color: BLUE")

                    elif pen_option == "THIN":
                        pen_thickness = 2
                        print("Pen thickness: THIN")

                    elif pen_option == "THICK":
                        pen_thickness = 8
                        print("Pen thickness: THICK")

                    elif pen_option == "BACK":
                        show_pen_settings = False
                        current_pen_hover = None
                        pen_hover_start = None

                    activated_pen_option = pen_option
            if active_mode == "DRAW" and previous_point is not None:
                cv2.line(
                    canvas,
                    previous_point,
                    smooth_point,
                    pen_color,
                    pen_thickness,
                    cv2.LINE_AA
                )

            elif active_mode == "ERASER" and previous_point is not None:
                cv2.line(
                    canvas,
                    previous_point,
                    smooth_point,
                    (0, 0, 0),
                    25,
                    cv2.LINE_AA
                )

            previous_point = smooth_point

    else:
        # Stop drawing when the marker disappears.
        previous_point = None
        smooth_point = None

    # Combine the drawing and cursor.
    display = cv2.add(canvas, board)

    cv2.imshow("Virtual Whiteboard - Red Marker", display)
    cv2.imshow("Red Detection Mask", mask)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("c"):
        canvas[:] = 0
        previous_point = None

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
