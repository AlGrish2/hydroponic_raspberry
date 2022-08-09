from dataclasses import dataclass
from typing import Protocol

import numpy as np

from detector.base import DetectionMeta

@dataclass
class ClassificationMeta:
    label: str
    proba: float

class Classifier(Protocol):

    def predict(self, image: np.ndarray, detection: DetectionMeta = None) -> list[ClassificationMeta]:
        pass