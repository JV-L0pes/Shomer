# shomer/domain/entities/face.py

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Face:
    bbox: Tuple[int, int, int, int]
