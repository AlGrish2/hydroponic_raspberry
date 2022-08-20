from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol, List

import numpy as np

@dataclass
class DetectionMeta:
    x_min: int
    y_min: int
    x_max: int
    y_max: int
    crop: np.ndarray

class Detector:
    def __init__(
        self, 
        model_path: str, 
        conf_thresh: float, 
        iou_thresh: float, 
        visibility_zone: tuple,
        ):

        self.model_path = model_path
        self.conf_thresh = conf_thresh
        self.iou_thresh = iou_thresh
        self.detection_model = self._load_model()
        self.visibility_zone = [i for i in range(visibility_zone[0], visibility_zone[1]+1)]

    def _load_model(self):
        pass
    
    @abstractmethod
    def predict(self, image: np.ndarray) -> List[DetectionMeta]:
        pass


class DummyDetector(Detector):

    def predict(self, image: np.ndarray) -> List[DetectionMeta]:
        preds = []
        raw_dummy_preds = (10, 10, 100, 100), (50, 50, 100, 100)
        for rdp in raw_dummy_preds:
            x_min, y_min, x_max, y_max = rdp
            pred = DetectionMeta(
                x_min,
                y_min,
                x_max,
                y_max,
                image[int(x_max):int(y_max), int(x_min):int(y_min)]
                )
            preds.append(pred)
        return preds
            