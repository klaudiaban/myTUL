import cv2

polygon_points = []


def mouse_callback(event, x, y, flags, param):
    global polygon_points
    if event == cv2.EVENT_LBUTTONDOWN:
        polygon_points.append((x, y))


def select_polygon_area(cap):
    global polygon_points
    polygon_points = []

    ret, frame = cap.read()
    if not ret:
        print("Failed to read the video frame.")
        return []

    clone = frame.copy()
    cv2.namedWindow("Draw Polygon")
    cv2.setMouseCallback("Draw Polygon", mouse_callback)

    while True:
        temp_frame = clone.copy()
        if len(polygon_points) > 1:
            for i in range(len(polygon_points) - 1):
                cv2.line(
                    temp_frame, polygon_points[i], polygon_points[i + 1], (0, 255, 0), 2
                )
        for point in polygon_points:
            cv2.circle(temp_frame, point, 5, (0, 0, 255), -1)

        cv2.imshow("Draw Polygon", temp_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    return polygon_points
