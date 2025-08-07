# shomer/domain/entities/person.py

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Person:
    bbox: Tuple[int, int, int, int]
    confidence: float
