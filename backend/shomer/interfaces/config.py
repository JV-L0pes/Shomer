# shomer/interfaces/config.py

import os


class Config:
    @staticmethod
    def load():
        return {
            "ip_url": "http://192.168.15.5:4747/video",
            "yolo_model": os.getenv("YOLO_MODEL", "yolov8n.pt"),
            "conf_threshold": float(os.getenv("CONF_THRESHOLD", "0.5")),
            "window_title": os.getenv("WINDOW_TITLE", "Shomer - Real-time"),
            "colors": {
                "person": (0, 255, 255),
                "face": (255, 128, 0),
                "bg": (0, 0, 0),
                "text": (255, 255, 255),
            },
        }
