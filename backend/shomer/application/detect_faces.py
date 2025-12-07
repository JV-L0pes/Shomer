# shomer/application/detect_faces.py

from typing import List
import numpy as np
from shomer.domain.ports.detector import IFaceDetector
from shomer.domain.entities.face import Face
from shomer.domain.entities.person import Person


class DetectFacesUseCase:
    def __init__(self, detector: IFaceDetector):
        self.detector = detector

    def execute(self, frame: np.ndarray, people: List[Person]) -> List[Face]:
        raw_boxes = self.detector.detect(frame, people)
        return [Face(tuple(b)) for b in raw_boxes]
