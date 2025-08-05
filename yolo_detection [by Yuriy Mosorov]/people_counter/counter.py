from utils.video_loader import load_video
from utils.yolo_detector import YOLODetector
from utils.byte_tracker import NorfairTracker
from people_counter.state import TrackStateManager
from people_counter.drawing import DrawingHelper
from people_counter.logic import LineLogic
from config import config
import cv2


class ImprovedPeopleCounter:
    def __init__(self):
        if config["mode"] == "detection":
            self.video_path = 0
        else:
            self.video_path = config["video_path"]

        self.detector = YOLODetector(config["model_path"], float(config["conf_threshold"]))
        self.tracker = NorfairTracker(distance_threshold=80)
        self.state = TrackStateManager()
        self.logic = LineLogic(self.state)
        self.draw = DrawingHelper(self.state, self.logic)
        self.line_points = []
        self.polygon_points = []
        self.mode = config.get("mode", "line")
        self.run()

    def run(self):
        cap = load_video(self.video_path)
        if not cap:
            print("Failed to load video.")
            return

        ret, first_frame = cap.read()
        if not ret:
            print("Video read failed.")
            return

        if self.mode == "line":
            if not self.draw.setup_line_drawing(first_frame, self.line_points):
                print("Line setup failed.")
                return
        elif self.mode == "polygon":
            if not self.draw.setup_polygon_drawing(first_frame, self.polygon_points):
                print("Polygon setup failed.")
                return

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame_count = 0
        print("Starting people detection... Press 'q' to quit, 'r' to reset counters")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            detections = self.detector.detect(frame)
            tracked_objects = self.tracker.update(detections)

            current_ids = []

            for cx, cy, track_id in tracked_objects:
                current_ids.append(track_id)
                self.state.update_position(track_id, (cx, cy))

                if self.mode == "line":
                    self.logic.check_line_crossing(track_id, self.line_points)
                    self.logic.reset_counting_state(track_id, self.line_points)

                self.draw.draw_track_info(frame, (cx, cy), track_id, self.line_points)

            if self.mode == "line":
                self.draw.draw_counting_line(frame, self.line_points)
                self.draw.draw_counter_display(frame)
            elif self.mode == "polygon":
                self.draw.draw_polygon_area(frame, self.polygon_points)
                self.draw.draw_polygon_count_display(frame, self.polygon_points)
            else:
                cv2.putText(
                    frame, "DETECTION ONLY", (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 255, 255), 2
                )

            if frame_count % 30 == 0:
                self.state.cleanup_old_tracks(current_ids)

            cv2.imshow("Enhanced People Counter", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.state.reset_counters()
                print("Counters reset.")

        cap.release()
        cv2.destroyAllWindows()
        self.state.print_summary()