from detector.base import Detector, DetectionMeta

from typing import List

import numpy as np
import cv2
import torch

import config


class PlantsDetector(Detector):

    def _load_model(self):
        return torch.hub.load('ultralytics/yolov5', 'custom', path=self.model_path)

    def predict(self, image: np.ndarray):
        predicts = self.detection_model(image).xyxy
        
        return [
            [
                DetectionMeta(
                    x_min = int(box[0]),
                    y_min = int(box[1]),
                    x_max = int(box[2]),
                    y_max = int(box[3]),
                    size = int((box[2]- box[0]) * (box[3] - box[1]) * (box[1] / image.shape[0]) ** 2),
                    crop = image[int(box[2]):int(box[3]), int(box[0]):int(box[1])]
                )
                for box in row 
                if (box[4] > self.conf_thresh) and (int(box[0]) > config.visibility_zone[0]) and (int(box[2]) < config.visibility_zone[1])
            ]
            for row in predicts
        ][0]
