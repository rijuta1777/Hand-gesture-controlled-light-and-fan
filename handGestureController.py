import cv2
import mediapipe as mp
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Initialize hand detector
detector = HandDetector(detectionCon=0.6, maxHands=2)

# Open webcam
video = cv2.VideoCapture(0)

# Initial values
fan_speed = 0
light_brightness = 0
angle = 0  # Fan rotation angle

while True:
    ret, frame = video.read()
    if not ret:
        print("Camera Error!")
        break

    frame = cv2.flip(frame, 1)  # Mirror effect
    hands, img = detector.findHands(frame)  # Detect hands

    if hands:  # Update values only when hands are detected
        for hand in hands:
            fingerUp = detector.fingersUp(hand)
            num_fingers = sum(fingerUp)  # Count raised fingers
            hand_type = hand["type"]  # 'Left' or 'Right'

            # Right Hand → Fan Control
            if hand_type == "Right":
                fan_speed = num_fingers
                print(f"Fan Speed Set: {fan_speed}")

            # Left Hand → Light Control
            elif hand_type == "Left":
                light_brightness = num_fingers
                print(f"Lights ON: {light_brightness}")

    # Draw Virtual Fan (Bigger)
    fan_center = (500, 300)
    blade_length = 120  # Increased size
    fan_color = (150, 150, 150)  # Standard fan color (gray)

    speed_factor = [0, 5, 10, 15, 25, 40]  # Fan speed levels
    angle = (angle + speed_factor[fan_speed]) % 360  # Keep angle in 0-360

    for i in range(3):  # 3 Blades
        blade_angle = np.radians(angle + i * 120)
        x = int(fan_center[0] + blade_length * np.cos(blade_angle))
        y = int(fan_center[1] + blade_length * np.sin(blade_angle))
        cv2.line(frame, fan_center, (x, y), fan_color, 10)  # Increased thickness

    cv2.circle(frame, fan_center, 15, (50, 50, 50), -1)  # Bigger Fan center

    # Display Light Brightness (Bigger White Circle)
    light_intensity = min(255, light_brightness * 50)
    circle_size = 60 + (light_brightness * 25)  # Increased size dynamically
    cv2.circle(frame, (150, 300), circle_size, (light_intensity, light_intensity, light_intensity), -1)

    # Display Output
    cv2.putText(frame, f"Fan Speed: {fan_speed}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
    cv2.putText(frame, f"Lights: {light_brightness}", (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

    cv2.imshow("Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
