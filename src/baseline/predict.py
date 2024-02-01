from ultralytics import YOLO
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

model = YOLO("../Yolo-Weights/yolov8n.pt")

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)