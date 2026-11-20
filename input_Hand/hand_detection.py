
import cv2
import mediapipe as mp

# 1. Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 2. Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not found")
    hands.close()
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        print("Cannot read camera frame")
        break

    # 3. Mirror the camera image
    frame = cv2.flip(frame, 1)

    # 4. Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 5. Detect hand landmarks
    results = hands.process(rgb_frame)

    # 6. Check if a hand is detected
    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw all 21 landmarks
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            h, w, _ = frame.shape

            # Get index fingertip (landmark 8)
            index_tip = hand_landmarks.landmark[8]

            index_x = int(index_tip.x * w)
            index_y = int(index_tip.y * h)

            # Get wrist (landmark 0)
            wrist = hand_landmarks.landmark[0]

            wrist_x = int(wrist.x * w)
            wrist_y = int(wrist.y * h)

            # Draw index fingertip
            cv2.circle(
                frame,
                (index_x, index_y),
                10,
                (0, 0, 255),
                -1
            )

            # Display coordinates
            cv2.putText(
                frame,
                f"Index: ({index_x}, {index_y})",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                f"Wrist: ({wrist_x}, {wrist_y})",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

    else:
        cv2.putText(
            frame,
            "No hand detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

    # 7. Display camera
    cv2.imshow("MediaPipe Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 8. Release resources
cap.release()
hands.close()
cv2.destroyAllWindows()
