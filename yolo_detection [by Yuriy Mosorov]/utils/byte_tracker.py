import numpy as np
from norfair import Detection, Tracker
from collections import deque, defaultdict


class NorfairTracker:
    def __init__(self, distance_threshold=60):
        self.tracker = Tracker(
            distance_function=self._enhanced_distance,
            distance_threshold=distance_threshold,
            hit_counter_max=15,
            initialization_delay=3,
            past_detections_length=25,
            pointwise_hit_counter_max=4,
        )

        self.track_positions = {}
        self.track_histories = defaultdict(lambda: deque(maxlen=30))
        self.track_velocities = {}
        self.track_confidences = defaultdict(float)
        self.last_seen = {}

        self.position_predictors = {}

    def _enhanced_distance(self, detection, tracked_object):
        euclidean_dist = np.linalg.norm(detection.points - tracked_object.estimate)

        track_id = getattr(tracked_object, "id", None)

        if track_id is not None and track_id in self.track_velocities:
            velocity = self.track_velocities[track_id]
            predicted_pos = tracked_object.estimate[0] + velocity
            predicted_dist = np.linalg.norm(detection.points[0] - predicted_pos)

            final_distance = 0.7 * euclidean_dist + 0.3 * predicted_dist

            confidence = self.track_confidences.get(track_id, 0.5)
            final_distance *= 2.0 - confidence

            return final_distance

        return euclidean_dist

    def _update_velocity(self, track_id, current_pos):
        if track_id not in self.track_histories:
            self.track_velocities[track_id] = np.array([0.0, 0.0])
            return

        history = list(self.track_histories[track_id])
        if len(history) >= 2:
            recent_positions = history[-3:] if len(history) >= 3 else history[-2:]
            velocities = []

            for i in range(1, len(recent_positions)):
                vel = np.array(recent_positions[i]) - np.array(recent_positions[i - 1])
                velocities.append(vel)

            if velocities:
                avg_velocity = np.mean(velocities, axis=0)

                if track_id in self.track_velocities:
                    self.track_velocities[track_id] = (
                        0.7 * self.track_velocities[track_id] + 0.3 * avg_velocity
                    )
                else:
                    self.track_velocities[track_id] = avg_velocity

    def _update_confidence(self, track_id, detection_confidence):
        current_confidence = self.track_confidences[track_id]

        if track_id in self.track_histories and len(self.track_histories[track_id]) > 5:
            consistency_bonus = 0.1
        else:
            consistency_bonus = 0.0

        new_confidence = 0.8 * current_confidence + 0.2 * (
            detection_confidence + consistency_bonus
        )
        self.track_confidences[track_id] = min(1.0, new_confidence)

    def _predict_missing_tracks(self):
        current_time = len(self.last_seen)

        predicted_detections = []
        for track_id, last_time in self.last_seen.items():
            frames_missing = current_time - last_time

            if frames_missing <= 5 and track_id in self.track_velocities:
                last_pos = self.track_positions.get(track_id)
                if last_pos is not None:
                    velocity = self.track_velocities[track_id]
                    predicted_pos = np.array(last_pos) + velocity * frames_missing

                    virtual_detection = Detection(
                        points=np.array([predicted_pos]),
                        scores=np.array([self.track_confidences.get(track_id, 0.3)]),
                    )
                    predicted_detections.append((virtual_detection, track_id))

        return predicted_detections

    def update(self, detections):
        norfair_detections = []
        detection_confidences = []

        for (x1, y1, x2, y2), conf in detections:
            center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2

            width, height = x2 - x1, y2 - y1
            area = width * height

            detection = Detection(
                points=np.array([[center_x, center_y]]),
                scores=np.array([conf]),
                data={"bbox": (x1, y1, x2, y2), "area": area},
            )
            norfair_detections.append(detection)
            detection_confidences.append(conf)

        tracked_objects = self.tracker.update(detections=norfair_detections)

        results = []
        current_frame_tracks = set()

        for i, obj in enumerate(tracked_objects):
            if hasattr(obj, "estimate") and obj.estimate is not None:
                cx, cy = obj.estimate[0]
                track_id = obj.id
                current_frame_tracks.add(track_id)

                pos = (int(cx), int(cy))
                self.track_positions[track_id] = pos
                self.track_histories[track_id].append(pos)
                self.last_seen[track_id] = len(self.last_seen)

                self._update_velocity(track_id, pos)

                if i < len(detection_confidences):
                    self._update_confidence(track_id, detection_confidences[i])

                results.append((int(cx), int(cy), track_id))

        self._cleanup_old_tracks(current_frame_tracks)

        return results

    def _cleanup_old_tracks(self, current_tracks, max_frames_missing=30):
        current_time = len(self.last_seen)

        tracks_to_remove = []
        for track_id, last_time in self.last_seen.items():
            if (
                track_id not in current_tracks
                and (current_time - last_time) > max_frames_missing
            ):
                tracks_to_remove.append(track_id)

        for track_id in tracks_to_remove:
            self.track_positions.pop(track_id, None)
            self.track_velocities.pop(track_id, None)
            self.track_confidences.pop(track_id, None)
            self.last_seen.pop(track_id, None)
            if track_id in self.track_histories:
                del self.track_histories[track_id]

    def get_track_info(self, track_id):
        return {
            "position": self.track_positions.get(track_id),
            "velocity": self.track_velocities.get(track_id),
            "confidence": self.track_confidences.get(track_id, 0.0),
            "history_length": len(self.track_histories.get(track_id, [])),
            "last_seen": self.last_seen.get(track_id, 0),
        }
