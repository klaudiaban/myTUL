import cv2

def load_video(video_path):
    if video_path == "0":
        video_path = 0
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Cannot open video: {video_path}")
        return None
    return cap