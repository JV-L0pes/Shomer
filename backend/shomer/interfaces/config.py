# shomer/interfaces/config.py

import os


class Config:
    @staticmethod
    def load():
        return {
            # Sem default; a URL virá via API moderna
            "ip_url": os.getenv("DEFAULT_IP_CAMERA_URL", ""),
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
