
import cv2
import mediapipe as mp
import numpy as np

from coordinate_mapping import map_point, matrix, width, height



# 1. INITIALIZE MEDIAPIPE


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)


# 2. INITIALIZE CAMERA


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    hands.close()
    raise RuntimeError("Cannot open camera")



# 3. DRAWING SETTINGS


canvas = np.zeros((height, width, 3), dtype=np.uint8)

pen_color = (0, 0, 255)  # Red
pen_thickness = 5

previous_point = None
smoothed_point = None

is_drawing = False

# Smoothing factor
SMOOTHING = 0.35

# Pinch thresholds relative to hand size
PINCH_START = 0.30
PINCH_STOP = 0.40



# 4. MAIN LOOP


while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Keep the same orientation as calibration
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand landmarks
    results = hands.process(rgb_frame)

    # Apply perspective transformation
    warped = cv2.warpPerspective(
        frame,
        matrix,
        (width, height)
    )

    board_point = None

    
    # 5. HAND DETECTION
    

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]
        landmarks = hand_landmarks.landmark

        # Draw hand landmarks
        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        # Get fingertips
        thumb = landmarks[4]
        index = landmarks[8]

        # Get wrist and middle finger MCP for hand scale
        wrist = landmarks[0]
        middle_mcp = landmarks[9]

        # Convert normalized coordinates to pixels
        h, w = frame.shape[:2]

        index_x = int(index.x * w)
        index_y = int(index.y * h)

        thumb_x = int(thumb.x * w)
        thumb_y = int(thumb.y * h)

        wrist_x = int(wrist.x * w)
        wrist_y = int(wrist.y * h)

        middle_x = int(middle_mcp.x * w)
        middle_y = int(middle_mcp.y * h)

        
        # 6. VISUALIZE FINGERTIPS
        

        # Thumb = GREEN
        cv2.circle(
            frame,
            (thumb_x, thumb_y),
            10,
            (0, 255, 0),
            -1
        )

        # Index = BLUE
        cv2.circle(
            frame,
            (index_x, index_y),
            10,
            (255, 0, 0),
            -1
        )

        # Fixed legend to avoid overlapping labels
        cv2.putText(
            frame,
            "GREEN: THUMB",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "BLUE: INDEX - PEN",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 0, 0),
            2
        )

        
        # 7. RELATIVE PINCH DETECTION
        

        # Distance between thumb and index
        pinch_distance = np.hypot(
            thumb_x - index_x,
            thumb_y - index_y
        )

        # Estimate hand size using wrist and middle MCP
        hand_size = np.hypot(
            middle_x - wrist_x,
            middle_y - wrist_y
        )

        # Avoid division by zero
        if hand_size > 0:

            pinch_ratio = pinch_distance / hand_size

        else:

            pinch_ratio = 1.0

        # Hysteresis: different start and stop thresholds
        if not is_drawing and pinch_ratio < PINCH_START:

            is_drawing = True
            previous_point = None
            smoothed_point = None

        elif is_drawing and pinch_ratio > PINCH_STOP:

            is_drawing = False
            previous_point = None
            smoothed_point = None

        
        # 8. MAP INDEX TO VIRTUAL BOARD
        

        # Only the index controls the pointer
        board_point = map_point(index_x, index_y)

        if board_point is not None and is_drawing:

            new_point = np.array(
                board_point,
                dtype=float
            )

            # Exponential smoothing
            if smoothed_point is None:

                smoothed_point = new_point

            else:

                smoothed_point = (
                    SMOOTHING * new_point
                    + (1 - SMOOTHING) * smoothed_point
                )

            current_point = tuple(
                np.round(smoothed_point).astype(int)
            )

            # Draw continuous line
            if previous_point is not None:

                cv2.line(
                    canvas,
                    previous_point,
                    current_point,
                    pen_color,
                    pen_thickness,
                    cv2.LINE_AA
                )

            # Fill small gaps
            cv2.circle(
                canvas,
                current_point,
                pen_thickness // 2,
                pen_color,
                -1,
                cv2.LINE_AA
            )

            previous_point = current_point

        else:

            previous_point = None
            smoothed_point = None

    else:

        # Reset when hand disappears
        is_drawing = False
        previous_point = None
        smoothed_point = None

    
    # 9. DISPLAY VIRTUAL BOARD
    

    output = cv2.add(warped, canvas)

    # Display index cursor
    if board_point is not None:

        cv2.circle(
            output,
            board_point,
            8,
            (255, 255, 0),
            -1,
            cv2.LINE_AA
        )

    # Display mode
    status = "DRAWING" if is_drawing else "POINTING"

    cv2.putText(
        output,
        f"Mode: {status}",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    # Keyboard instructions
    cv2.putText(
        output,
        "1: Red | 2: Blue | C: Clear | Q: Quit",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    cv2.imshow("Hand Detection", frame)
    cv2.imshow("Interactive Virtual Board", output)

    
    # 10. KEYBOARD CONTROLS
    

    key = cv2.waitKey(1) & 0xFF

    if key == ord('1'):

        pen_color = (0, 0, 255)
        previous_point = None
        smoothed_point = None

    elif key == ord('2'):

        pen_color = (255, 0, 0)
        previous_point = None
        smoothed_point = None

    elif key in (ord('c'), ord('C')):

        canvas[:] = 0
        previous_point = None
        smoothed_point = None

    elif key == ord('q'):

        break



# 11. RELEASE RESOURCES


cap.release()
hands.close()
cv2.destroyAllWindows()
