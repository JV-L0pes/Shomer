# shomer/infrastructure/detectors/mp_detector.py

import cv2
import mediapipe as mp
from typing import List, Tuple
from shomer.domain.ports.detector import IFaceDetector
from shomer.domain.entities.person import Person


class MediaPipeFaceDetector(IFaceDetector):
    def __init__(self):
        self.detector = mp.solutions.face_detection.FaceDetection()

    def detect(self, frame, people: List[Person]) -> List[Tuple[int, int, int, int]]:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.detector.process(img)
        boxes: List[Tuple[int, int, int, int]] = []
        if res.detections:
            h, w, _ = frame.shape
            for det in res.detections:
                bb = det.location_data.relative_bounding_box
                x1 = int(bb.xmin * w)
                y1 = int(bb.ymin * h)
                x2 = x1 + int(bb.width * w)
                y2 = y1 + int(bb.height * h)
                boxes.append((x1, y1, x2, y2))
        return boxes
