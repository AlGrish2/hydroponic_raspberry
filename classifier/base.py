from dataclasses import dataclass
from typing import Protocol

import numpy as np

from detector.base import DetectionMeta

@dataclass
class ClassificationMeta:
    deffect_0: float
    deffect_1: float
    deffect_2: float

class Classifier:
    def __init__(self, model_path: str, conf_thresh):
        self.model_path = model_path
        self.conf_thresh = conf_thresh
        self.model = self._load_model()
    
    def _load_model(self):
        pass

    def predict(self, image: np.ndarray) -> ClassificationMeta:
        pass


class DummyClassifier(Classifier):
    def predict(self, image: np.ndarray) -> ClassificationMeta:
        return ClassificationMeta(0.1, 0.2, 0.3)