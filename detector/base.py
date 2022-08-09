from dataclasses import dataclass
from typing import Protocol

import numpy as np

@dataclass
class DetectionMeta:
    x_min: int
    y_min: int
    x_max: int
    y_max: int
    crop: np.ndarray

class Detector(Protocol):

    def predict(self, image) -> list[DetectionMeta]:
        pass