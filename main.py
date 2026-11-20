
import cv2
import numpy as np

# 1. Open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not found")
    exit()


# 2. Define the red color ranges in HSV
lower_red1 = np.array([0, 100, 50])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 100, 50])
upper_red2 = np.array([179, 255, 255])


while True:

    # 3. Capture a frame
    ret, frame = cap.read()

    if not ret:
        break

    # 4. Mirror the image
    frame = cv2.flip(frame, 1)

    # 5. Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 6. Create a binary mask
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = cv2.bitwise_or(mask1, mask2)
     
    # Remove small noise from the mask
    kernel = np.ones((3, 3), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
  )
    # 7. Find the detected pixels
    ys, xs = np.where(mask == 255)

    # 8. Calculate and display the center
    if len(xs) > 0:
        x = int(np.mean(xs))
        y = int(np.mean(ys))

        cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)

        cv2.putText(frame, f"({x}, {y})",
                    (x + 15, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)

    # 9. Display the results
    cv2.imshow("Camera", frame)
    cv2.imshow("Red Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 10. Release resources
cap.release()
cv2.destroyAllWindows()
