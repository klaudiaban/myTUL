import numpy as np
import cv2

class LineLogic:
    def __init__(self, state_manager):
        self.state = state_manager

    def average_point(self, points):
        if not points:
            return (0, 0)
        x = int(np.mean([p[0] for p in points]))
        y = int(np.mean([p[1] for p in points]))
        return (x, y)

    def get_line_side(self, point, line_points):
        if len(line_points) != 2:
            return None
        p1, p2 = line_points
        return np.sign(
            (p2[0] - p1[0]) * (point[1] - p1[1]) - (p2[1] - p1[1]) * (point[0] - p1[0])
        )

    def is_near_line(self, point, line_points, max_distance=100):
        if len(line_points) != 2:
            return False
        p1, p2 = line_points
        A, B = p2[1] - p1[1], p1[0] - p2[0]
        C = p2[0] * p1[1] - p1[0] * p2[1]
        distance = abs(A * point[0] + B * point[1] + C) / np.sqrt(A**2 + B**2)
        return distance <= max_distance

    def crosses_segment(self, pt1, pt2, line_points):
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        A, B = pt1, pt2
        C, D = line_points
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    def check_line_crossing(self, track_id, line_points):
        if self.state.has_been_counted(track_id):
            return False

        history = self.state.get_history(track_id)
        if len(history) < 5:
            return False

        recent = list(history)[-5:]
        current_avg = self.average_point(recent[-3:])
        previous_avg = self.average_point(recent[:3])
        current_side = self.get_line_side(current_avg, line_points)
        previous_side = self.get_line_side(previous_avg, line_points)

        if (
            previous_side == current_side
            or previous_side is None
            or current_side is None
        ):
            return False

        if not self.crosses_segment(previous_avg, current_avg, line_points):
            return False

        if previous_side < current_side:
            self.state.entry_count += 1
        else:
            self.state.exit_count += 1

        self.state.set_counted(track_id, current_side)
        return True

    def reset_counting_state(self, track_id, line_points):
        history = self.state.get_history(track_id)
        if len(history) >= 10:
            recent = list(history)[-5:]
            if all(not self.is_near_line(pos, line_points, 150) for pos in recent):
                self.state.reset_counting_state(track_id)

    def get_people_in_polygon(self, polygon):
        inside_ids = []
        for track_id, pos in self.state.positions.items():
            if cv2.pointPolygonTest(np.array(polygon, dtype=np.int32), pos, False) >= 0:
                inside_ids.append(track_id)
        return inside_ids