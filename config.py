# config.py

# Path to your YOLOv8 person model
YOLO_MODEL = "yolov8n.pt"

# Which face detector you're using ('mediapipe' for MediaPipe, or 'insightface' if you switched)
FACE_DETECTOR = "mediapipe"

# Confidence threshold for person detection
CONFIDENCE_THRESHOLD = 0.5

# config.py
IP_CAMERA_URL = "http://192.168.15.5:4747/video"
# ou, se isso não funcionar, tente:
# IP_CAMERA_URL = 'http://192.168.15.5:4747/mjpeg'


# Janela de cálculo de FPS (não usado no render final)
SOFTWARE_FPS_WINDOW = 60
