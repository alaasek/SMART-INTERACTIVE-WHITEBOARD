
import cv2
import numpy as np

from coordinate_mapping import width, height

# Menu configuration
MENU_WIDTH = 180
MENU_BACKGROUND = (45, 45, 45)
BUTTON_COLOR = (70, 70, 70)
TEXT_COLOR = (255, 255, 255)

BUTTONS = [
    "DRAW",
    "PEN SETTINGS",
    "ERASER",
    "CLEAR BOARD"
]


def draw_menu(board):
    """Display the interactive menu on the virtual board."""

    x1 = 10
    y1 = 10
    x2 = x1 + MENU_WIDTH
    y2 = 250

    # Menu background
    cv2.rectangle(
        board,
        (x1, y1),
        (x2, y2),
        MENU_BACKGROUND,
        -1
    )

    # Menu title
    cv2.putText(
        board,
        "SMART BOARD",
        (x1 + 10, y1 + 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        TEXT_COLOR,
        1
    )

    # Draw buttons
    button_height = 45

    for i, label in enumerate(BUTTONS):
        button_y = y1 + 40 + i * 50

        cv2.rectangle(
            board,
            (x1 + 10, button_y),
            (x2 - 10, button_y + button_height),
            BUTTON_COLOR,
            -1
        )

        cv2.putText(
            board,
            label,
            (x1 + 20, button_y + 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            TEXT_COLOR,
            1
        )

    return board

def get_hovered_button(point):
    """Return the button under the marker, if any."""

    if point is None:
        return None

    x, y = point

    x1 = 20
    x2 = MENU_WIDTH - 10
    button_height = 45

    for i, label in enumerate(BUTTONS):
        y1 = 50 + i * 50
        y2 = y1 + button_height

        if x1 <= x <= x2 and y1 <= y <= y2:
            return label

    return None
def draw_pen_settings(board):
    x1, y1 = 220, 10
    x2, y2 = 480, 200

    cv2.rectangle(board, (x1, y1), (x2, y2), (45, 45, 45), -1)

    cv2.putText(
        board, "PEN SETTINGS",
        (x1 + 15, y1 + 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1
    )

    options = ["RED", "BLUE", "THIN", "THICK", "BACK"]

    for i, option in enumerate(options):
        y = y1 + 50 + i * 28

        cv2.putText(
            board, option,
            (x1 + 25, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1
        )

    return board

def get_hovered_pen_option(point):
    if point is None:
        return None

    x, y = point

    options = ["RED", "BLUE", "THIN", "THICK", "BACK"]

    for i, option in enumerate(options):
        y1 = 45 + i * 28
        y2 = 72 + i * 28

        if 230 <= x <= 470 and y1 <= y <= y2:
            return option

    return None