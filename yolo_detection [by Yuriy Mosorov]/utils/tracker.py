import numpy as np
from collections import deque


class Track:
    def __init__(self, track_id, bbox):
        self.id = track_id
        self.bbox = bbox
        self.missing_frames = 0
        self.history = deque(maxlen=30)

    def update(self, new_bbox):
        self.bbox = new_bbox
        self.history.append(new_bbox)
        self.missing_frames = 0

    def predict(self):
        self.missing_frames += 1


class TrackerLite:
    def __init__(self, iou_threshold=0.3, max_missing=10):
        self.tracks = []
        self.next_id = 0
        self.iou_threshold = iou_threshold
        self.max_missing = max_missing

    def iou(self, boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        interArea = max(0, xB - xA) * max(0, yB - yA)
        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
        return interArea / float(boxAArea + boxBArea - interArea + 1e-6)

    def update(self, detections):
        matched = set()
        unmatched_tracks = set(range(len(self.tracks)))
        unmatched_detections = set(range(len(detections)))
        iou_matrix = np.zeros((len(self.tracks), len(detections)), dtype=np.float32)

        for i, track in enumerate(self.tracks):
            for j, det in enumerate(detections):
                iou_val = self.iou(track.bbox, det)
                iou_matrix[i, j] = iou_val

        while True:
            if iou_matrix.size == 0:
                break
            i, j = np.unravel_index(np.argmax(iou_matrix), iou_matrix.shape)
            if iou_matrix[i, j] < self.iou_threshold:
                break
            self.tracks[i].update(detections[j])
            matched.add((i, j))
            unmatched_tracks.discard(i)
            unmatched_detections.discard(j)
            iou_matrix[i, :] = -1
            iou_matrix[:, j] = -1

        for i in unmatched_tracks:
            self.tracks[i].predict()

        self.tracks = [t for t in self.tracks if t.missing_frames <= self.max_missing]

        for j in unmatched_detections:
            self.tracks.append(Track(self.next_id, detections[j]))
            self.next_id += 1

        results = []
        for track in self.tracks:
            x1, y1, x2, y2 = track.bbox
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            results.append((cx, cy, track.id, track.bbox))

        return results
