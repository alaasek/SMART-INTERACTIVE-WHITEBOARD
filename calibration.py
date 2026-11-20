
import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not found")
    exit()

points = []

def select_corner(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        print(f"Point {len(points)}: ({x}, {y})")

cv2.namedWindow("Calibration")
cv2.setMouseCallback("Calibration", select_corner)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    for i, point in enumerate(points):
        cv2.circle(frame, point, 7, (0, 255, 0), -1)
        cv2.putText(
            frame, str(i + 1),
            (point[0] + 10, point[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (0, 255, 0), 2
        )

    cv2.imshow("Calibration", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("Selected corners:", points)
