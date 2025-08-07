# shomer/domain/ports/detector.py

from abc import ABC, abstractmethod
import numpy as np
from typing import Any, List
from shomer.domain.entities.person import Person


class IPersonDetector(ABC):
    @abstractmethod
    def detect(self, frame: np.ndarray) -> Any:
        """Retorna objeto bruto de detecção de pessoas."""
        pass


class IFaceDetector(ABC):
    @abstractmethod
    def detect(self, frame: np.ndarray, people: List[Person]) -> List[tuple]:
        """Retorna lista de bboxes de faces."""
        pass
