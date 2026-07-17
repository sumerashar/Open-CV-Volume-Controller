import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

# Class to handle the drag-and-drop logic
class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor, dist):
        cx, cy = self.posCenter
        w, h = self.size

        # Check if cursor is inside the rectangle
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            # If fingers are pinched, update the center
            if dist < 30:
                self.posCenter = cursor[0], cursor[1]
                return (0, 0, 255) # Red: Dragging
            return (0, 255, 0) # Green: Hovering
        return (255, 0, 255) # Purple: Idle

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
rectList = []
for i in range(4):
    rectList.append(DragRect([i*250+150,150]))


    
rect = DragRect([150, 150])
 

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    
    colorR = (255, 0, 255) # Default color
    
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        # Calculate distance for the pinch gesture
        dist, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        cursor = lmList[8]
        
        # Update rect state and get the new color
        for rect in rectList:
            colorR = rect.update(cursor, dist)

    # Draw the rectangle using the updated rect position
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()