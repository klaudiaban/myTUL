import cv2
import numpy as np
from config import config


class DrawingHelper:
    def __init__(self, state, logic):
        self.state = state
        self.logic = logic

    def setup_line_drawing(self, frame, line_points):
        def line_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN and len(line_points) < 2:
                line_points.append((x, y))
                print(f"Point {len(line_points)}: ({x}, {y})")

        cv2.namedWindow("Setup Counting Line", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Setup Counting Line", line_callback)

        while True:
            display = frame.copy()
            for i, pt in enumerate(line_points):
                cv2.circle(display, pt, 8, (0, 0, 255), -1)
                cv2.putText(
                    display,
                    f"P{i+1}",
                    (pt[0] + 10, pt[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

            if len(line_points) == 2:
                self.draw_counting_line(display, line_points)
                cv2.putText(
                    display,
                    "Press 'c' to continue",
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                )

            cv2.putText(
                display,
                f"Click {2 - len(line_points)} more point(s)",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )
            cv2.imshow("Setup Counting Line", display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                return False
            elif key == ord("c") and len(line_points) == 2:
                break

        cv2.destroyAllWindows()
        return True

    def draw_counting_line(self, frame, line_points):
        if len(line_points) != 2:
            return
        p1, p2 = line_points
        cv2.line(frame, p1, p2, config["line_color"], config["line_thickness"])
        self.draw_direction_indicators(frame, p1, p2)
        cv2.circle(frame, p1, 6, (255, 255, 255), -1)
        cv2.circle(frame, p2, 6, (255, 255, 255), -1)

    def draw_direction_indicators(self, frame, p1, p2):
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        length = np.sqrt(dx * dx + dy * dy)
        if length == 0:
            return

        dx, dy = dx / length, dy / length
        perp_x, perp_y = -dy, dx

        mid_x = (p1[0] + p2[0]) // 2
        mid_y = (p1[1] + p2[1]) // 2

        offset = 60
        tip_length = 0.5

        entry_end = (int(mid_x + perp_x * offset), int(mid_y + perp_y * offset))
        cv2.arrowedLine(
            frame,
            (mid_x, mid_y),
            entry_end,
            config["entry_color"],
            3,
            tipLength=tip_length,
        )
        cv2.putText(
            frame,
            "ENTRY",
            (entry_end[0] + 10, entry_end[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            config["entry_color"],
            2,
        )

        exit_end = (int(mid_x - perp_x * offset), int(mid_y - perp_y * offset))
        cv2.arrowedLine(
            frame,
            (mid_x, mid_y),
            exit_end,
            config["exit_color"],
            3,
            tipLength=tip_length,
        )
        cv2.putText(
            frame,
            "EXIT",
            (exit_end[0] + 10, exit_end[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            config["exit_color"],
            2,
        )

    def draw_track_info(self, frame, point, track_id, line_points):
        cx, cy = point
        color = config["track_colors"][track_id % len(config["track_colors"])]
        cv2.circle(frame, (cx, cy), 8, (255, 255, 255), -1)
        cv2.circle(frame, (cx, cy), 8, color, 3)
        label = f"#{track_id}"
        (text_width, text_height), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_DUPLEX, 0.6, 1
        )
        cv2.rectangle(
            frame,
            (cx - text_width // 2 - 4, cy - text_height - 15),
            (cx + text_width // 2 + 4, cy - 5),
            config["bg_color"],
            -1,
        )
        cv2.putText(
            frame,
            label,
            (cx - text_width // 2, cy - 8),
            cv2.FONT_HERSHEY_DUPLEX,
            0.6,
            config["text_color"],
            1,
        )

        self.draw_trajectory(frame, track_id, color)

    def draw_counter_display(self, frame):
        height, width = frame.shape[:2]
        padding = 20
        section_spacing = 180

        cv2.rectangle(frame, (0, 0), (width, 80), config["counter_bg_color"], -1)

        y_base = 50

        cv2.putText(
            frame,
            "ENTRIES:",
            (padding, y_base),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            str(self.state.entry_count),
            (padding + 130, y_base),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            config["entry_color"],
            2,
        )

        cv2.putText(
            frame,
            "EXITS:",
            (padding + section_spacing, y_base),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            str(self.state.exit_count),
            (padding + section_spacing + 110, y_base),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            config["exit_color"],
            2,
        )

        net = self.state.entry_count - self.state.exit_count
        cv2.putText(
            frame,
            "NET:",
            (padding + section_spacing * 2, y_base),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            str(net),
            (padding + section_spacing * 2 + 80, y_base),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            "TRACKING:",
            (padding + section_spacing * 3, y_base),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            str(len(self.state.position_history)),
            (padding + section_spacing * 3 + 150, y_base),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (0, 255, 255),
            2,
        )

    def draw_trajectory(self, frame, track_id, color):
        points = self.state.get_trajectory(track_id)
        if len(points) < 2:
            return

        for i in range(1, len(points)):
            pt1, pt2 = points[i - 1], points[i]
            alpha = i / len(points)
            thickness = max(1, int(2 + 2 * alpha))
            faded_color = tuple(int(c * alpha + 50 * (1 - alpha)) for c in color)
            cv2.line(frame, pt1, pt2, faded_color, thickness)

    def get_people_in_polygon(self, polygon):
        inside_ids = []
        poly_np = np.array(polygon, dtype=np.int32)

        for track_id, history in self.state.position_history.items():
            if not history:
                continue
            latest_pos = history[-1]
            if cv2.pointPolygonTest(poly_np, latest_pos, False) >= 0:
                inside_ids.append(track_id)

        return inside_ids

    def setup_polygon_drawing(self, frame, polygon_points):
        def click(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                polygon_points.append((x, y))

        print("Click polygon corners. Press 'q' when done.")
        cv2.namedWindow("Polygon Selector")
        cv2.setMouseCallback("Polygon Selector", click)

        while True:
            temp = frame.copy()
            for pt in polygon_points:
                cv2.circle(temp, pt, 4, (0, 0, 255), -1)
            if len(polygon_points) > 1:
                for i in range(len(polygon_points) - 1):
                    cv2.line(temp, polygon_points[i], polygon_points[i + 1], (0, 255, 0), 2)
            if len(polygon_points) >= 3:
                cv2.line(temp, polygon_points[-1], polygon_points[0], (0, 255, 0), 2)

            cv2.imshow("Polygon Selector", temp)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyWindow("Polygon Selector")
        return len(polygon_points) >= 3

    def draw_polygon_area(self, frame, polygon_points):
        if len(polygon_points) >= 3:
            cv2.polylines(frame, [np.array(polygon_points, dtype=np.int32)], True, (0, 255, 0), 2)

    def draw_polygon_count_display(self, frame, polygon_points):
        inside_ids = self.get_people_in_polygon(polygon_points)
        text = f"IN AREA: {len(inside_ids)}"
        cv2.rectangle(frame, (10, frame.shape[0] - 50), (300, frame.shape[0] - 10), (0, 0, 0), -1)
        cv2.putText(
            frame,
            text,
            (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_DUPLEX,
            0.7,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )