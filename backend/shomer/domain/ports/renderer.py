# shomer/domain/ports/renderer.py

from abc import ABC, abstractmethod
import numpy as np
from typing import List
from shomer.domain.entities.person import Person
from shomer.domain.entities.face import Face


class IRenderer(ABC):
    @abstractmethod
    def render(
        self,
        frame: np.ndarray,
        people: List[Person],
        faces: List[Face],
        current_count: int,
        total_entered: int,
        total_exited: int,
    ) -> int:
        """Desenha no frame e retorna código da tecla pressionada."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Fecha janelas e libera recursos."""
        pass
