import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

# Initialize Camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize Detector
detector = HandDetector(detectionCon=0.8)
colorR = (255, 0, 255)

class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        # Ensure we only store the x and y coordinates
        self.posCenter = [posCenter[0], posCenter[1]]
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # If the index finger tip is in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and \
           cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = [cursor[0], cursor[1]]

rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    # Updated: findHands returns all hand data
    hands, img = detector.findHands(img)

    if hands:
        # Extract landmark list from the first detected hand
        hand1 = hands[0]
        lmList = hand1["lmList"]
        
        # Calculate distance using coordinates directly
        p1 = (lmList[8][0], lmList[8][1])
        p2 = (lmList[12][0], lmList[12][1])
        
        l, _, _ = detector.findDistance(p1, p2, img)
        
        if l < 30:
            cursor = lmList[8]
            for rect in rectList:
                rect.update(cursor)

    ## Draw Transparency
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        # Explicitly take only the first two values
        cx, cy = rect.posCenter[0], rect.posCenter[1]
        w, h = rect.size
        
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
                      (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    
    cv2.imshow("Image", out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()