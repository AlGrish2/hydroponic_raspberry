from detector.base import Detector, DetectionMeta
from config import x_start, x_end, confidence_treshold

from typing import List

import numpy as np
import cv2
import torch


class PlantsDetector(Detector):
    def __init__(self, model_path: str):
        self.visibility_zone = [i for i in range(x_start, x_end+1)]
        self.detection_model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)


    def predict(self, image: np.ndarray):
        predicts = self.detection_model(image).xyxy
        return [
        [
            DetectionMeta(
                x_min = int(box[0]),
                y_min = int(box[1]),
                x_max = int(box[2]),
                y_max = int(box[3]),
                crop = image[int(box[2]):int(box[3]), int(box[0]):int(box[1])]
            )
            for box in row if (box[4] > confidence_treshold) and (int(box[0]) in self.visibility_zone) and (int(box[2]) in self.visibility_zone)
        ]
        for row in predicts
    ]