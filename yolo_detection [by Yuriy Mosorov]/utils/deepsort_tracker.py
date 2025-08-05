from deep_sort_realtime.deepsort_tracker import DeepSort


class DeepSORTTracker:
    def __init__(self):
        self.tracker = DeepSort(max_age=30)

    def update(self, detections, frame):
        formatted_dets = []
        for det in detections:
            try:
                box, conf = det
                if len(box) == 4:
                    x1, y1, x2, y2 = box
                    w = x2 - x1
                    h = y2 - y1
                    formatted_dets.append([[x1, y1, w, h], conf])
            except Exception:
                continue

        if not formatted_dets:
            return []

        tracks = self.tracker.update_tracks(formatted_dets, frame=frame)

        results = []
        for track in tracks:
            if not track.is_confirmed():
                continue
            x1, y1, x2, y2 = map(int, track.to_ltrb())
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            results.append((cx, cy, track.track_id, (x1, y1, x2, y2)))
        return results
