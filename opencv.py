import cv2
import mediapipe as mp
import os

#based upon the distance between index and thumb, calulate the volume percentage and set it using amixer command.
# quite compatble to LINIUX OS, for windows you can use pycaw library to set the volume.
# 
MIN_DIST = 30
MAX_DIST = 200

Webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7
) 
drawing_utils = mp.solutions.drawing_utils 

while True:
    success, Image = Webcam.read()
    if not success:
        break
    
    Image = cv2.flip(Image, 1)
    frame_height, frame_width, _ = Image.shape
    rgb_image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    
    if output.multi_hand_landmarks:
        for hand in output.multi_hand_landmarks:
            drawing_utils.draw_landmarks(Image, hand, mp.solutions.hands.HAND_CONNECTIONS)
            
            # Extract coordinates for Index (8) and Thumb (4)
            x1 = int(hand.landmark[8].x * frame_width)
            y1 = int(hand.landmark[8].y * frame_height)
            x2 = int(hand.landmark[4].x * frame_width)
            y2 = int(hand.landmark[4].y * frame_height)

            # Euclidean distance
            distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5

            # Proportional Mapping: convert distance to 0-100 percentage
            percent = (distance - MIN_DIST) / (MAX_DIST - MIN_DIST)
            percent = max(0, min(1, percent)) # Clamp between 0 and 1
            volume_int = int(percent * 100)
            
            # Apply Volume
            os.system(f"amixer -D pulse sset Master {volume_int}%")

            # Draw visual feedback
            cv2.line(Image, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.circle(Image, (x1, y1), 8, (0, 255, 255), -1)
            cv2.circle(Image, (x2, y2), 8, (0, 0, 255), -1)
            cv2.putText(Image, f'{volume_int}%', (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Hand control Via Python", Image)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Webcam.release()
cv2.destroyAllWindows()