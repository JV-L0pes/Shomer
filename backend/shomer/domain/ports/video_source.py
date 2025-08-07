# shomer/domain/ports/video_source.py

from abc import ABC, abstractmethod
import numpy as np


class IVideoSource(ABC):
    @abstractmethod
    def read_frame(self) -> np.ndarray:
        """Retorna próximo frame BGR ou None."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Libera recursos."""
        pass
