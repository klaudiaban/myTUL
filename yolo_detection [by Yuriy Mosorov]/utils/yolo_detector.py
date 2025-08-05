from ultralytics import YOLO
from config import config


class YOLODetector:
    def __init__(self, model, conf_threshold):
        self.model = YOLO(model)
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        results = self.model(frame)[0]
        detections = []

        for box in results.boxes:
            if box.conf < self.conf_threshold:
                continue
            cls = int(box.cls)
            if cls != 0:
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf)
            detections.append(((x1, y1, x2, y2), conf))

        return detections
