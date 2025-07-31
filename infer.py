import os

# Silencia logs do ONNXRuntime antes de importá-lo
os.environ["ORT_LOG_LEVEL"] = "WARNING"

import threading
import cv2
import torch
from ultralytics import YOLO
from insightface.app import FaceAnalysis
from config import YOLO_MODEL, CONFIDENCE_THRESHOLD


class InferenceThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)

        # Person detector
        self.person_model = YOLO(YOLO_MODEL)
        self.person_model.fuse()
        if torch.cuda.is_available():
            self.person_model.model = self.person_model.model.half().to("cuda")

        # Face detector (RetinaFace via InsightFace)
        self.face_analyzer = FaceAnalysis(allowed_modules=["detection"])
        ctx_id = 0 if torch.cuda.is_available() else -1
        self.face_analyzer.prepare(ctx_id=ctx_id, det_size=(640, 640))

        self.frame = None
        self.results = None
        self.running = True

    def update_frame(self, frame):
        self.frame = frame

    def run(self):
        while self.running:
            if self.frame is None:
                continue

            bodies = self.person_model(
                self.frame, classes=[0], conf=CONFIDENCE_THRESHOLD
            )[0]

            # full-frame face detection
            face_objs = self.face_analyzer.get(self.frame)
            face_boxes = [tuple(map(int, f.bbox)) for f in face_objs]

            self.results = (bodies, face_boxes)
