config = {
    "model_path": "yolov8n.pt",
    # "video_path": "/Users/mosorov/Desktop/python/Yolo_detection_camera/data/PEOPLE_CITY.mp4",
    "video_path": "0",
    "line_color": (0, 255, 255),
    "line_thickness": 3,
    "track_colors": [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
        (128, 0, 128),
        (255, 165, 0),
    ],
    "text_color": (255, 255, 255),
    "bg_color": (0, 0, 0),
    "counter_bg_color": (50, 50, 50),
    "entry_color": (0, 255, 0),
    "exit_color": (0, 0, 255),
    "conf_threshold": 0.3,
    "mode": "polygon" #here is -detection (camera on laptop), -polygon and -line
}

