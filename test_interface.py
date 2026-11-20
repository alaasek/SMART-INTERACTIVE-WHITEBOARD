import cv2
import numpy as np

from coordinate_mapping import width, height
from interface import draw_menu

board = np.zeros((height, width, 3), dtype=np.uint8)

board = draw_menu(board)

cv2.imshow("Smart Interactive Whiteboard", board)

cv2.waitKey(0)
cv2.destroyAllWindows()