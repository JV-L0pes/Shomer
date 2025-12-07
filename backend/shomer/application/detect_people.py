# shomer/application/detect_people.py

from typing import List
import numpy as np
from shomer.domain.ports.detector import IPersonDetector
from shomer.domain.entities.person import Person


class DetectPeopleUseCase:
    def __init__(self, detector: IPersonDetector):
        self.detector = detector

    def execute(self, frame: np.ndarray) -> List[Person]:
        raw = self.detector.detect(frame)
        people: List[Person] = []
        for box, conf in zip(raw.boxes.xyxy, raw.boxes.conf):
            coords = tuple(map(int, box))
            people.append(Person(coords, float(conf)))
        return people
