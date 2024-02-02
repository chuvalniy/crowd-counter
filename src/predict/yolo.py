import math

import cv2
import cvzone
import numpy as np
from ultralytics import YOLO

from src.utils import scale_cross_lines
from src.utils import sort

cap = cv2.VideoCapture("../../data/test-video.mp4")
cap.set(cv2.CAP_PROP_FPS, 5)

model = YOLO("../Yolo-Weights/yolov8n.pt")

# Video width & height
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

enter_line, exit_line = scale_cross_lines("../../data/detections.json", width, height)

# Track enter & exit
entered = {}
exited = {}

enter_count = 0
exit_count = 0

# Hardcoded value to determine entry and exit boundaries.
cross_line_range = 5

# Tracking algorithm using SORT
tracker = sort.Sort(max_age=3, min_hits=3, iou_threshold=0.3)

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # Enter & exit lines.
    cv2.line(img, (enter_line[0], enter_line[1]), (enter_line[2], enter_line[3]), color=(255, 0, 0), thickness=2)
    cv2.line(img, (exit_line[0], exit_line[1]), (exit_line[2], exit_line[3]), color=(128, 128, 0), thickness=2)

    detections = np.empty((0, 5))

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = (int(c) for c in box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            conf = math.ceil((box.conf[0] * 100)) / 100

            cls = int(box.cls[0])
            if cls == 0:  # Person class
                curr_detections = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, curr_detections))

    tracking_result = tracker.update(detections)
    for r in tracking_result:
        x1, y1, x2, y2, idx = (int(c) for c in r)
        w, h = x2 - x1, y2 - y1

        cvzone.cornerRect(img, (x1, y1, w, h), l=9, colorR=(255, 0, 0))
        cvzone.putTextRect(img, f"{idx}", (max(0, x1), max(35, y1)), scale=0.6, thickness=1, offset=3)

        # Tracking points (Left bottom corner of a person box)
        cx, cy = x1, y2
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        # Check if a person crossed enter & exit lines.
        if enter_line[0] < cx < enter_line[2] and enter_line[1] - 5 < cy < enter_line[3] + 5:
            entered[idx] = entered.get(idx, 0) + 1
            if idx in exited:
                enter_count += 1
                exited.pop(idx)

        if exit_line[0] < cx < exit_line[2] and exit_line[1] - 5 < cy < exit_line[3] + 5:
            exited[idx] = exited.get(idx, 0) + 1
            if idx in entered:
                exit_count += 1
                entered.pop(idx)

    # Show current counting in a video.
    cvzone.putTextRect(img, f"Enter: {enter_count}", (10, 60), 1, 2)
    cvzone.putTextRect(img, f"Exit: {exit_count}", (10, 100), 1, 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
