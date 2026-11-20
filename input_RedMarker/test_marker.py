
import cv2
from marker_detection import detect_red_marker
from coordinate_mapping import map_point

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    mask, center = detect_red_marker(frame)

    if center is not None:
        x, y = center
        cv2.circle(frame, (x, y), 10, (0, 255, 0), 2)
        cv2.putText(
            frame, "RED MARKER",
            (x + 15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 255, 0), 2
        )
        board_point = map_point(center[0], center[1])

        if board_point is not None:
            bx, by = board_point

            cv2.circle(
                frame,
                center,
                8,
                (0, 255, 0),
                2
            )

            print("Camera:", center, "| Board:", board_point)

    cv2.imshow("Marker Detection", frame)
    cv2.imshow("Red Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
