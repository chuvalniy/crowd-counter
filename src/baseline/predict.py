import math

import cv2
import cvzone
from ultralytics import YOLO

cap = cv2.VideoCapture("../../data/test-video.mp4")

model = YOLO("../Yolo-Weights/yolov8n.pt")

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = (int(c) for c in box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            conf = math.ceil((box.conf[0] * 100)) / 100

            cls = int(box.cls[0])
            if cls == 0:  # Person class
                cvzone.cornerRect(img, (x1, y1, w, h), l=9)

                cx, cy = x1 + w // 2, y1 + h // 2
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
