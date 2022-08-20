from detector.base import Detector, DetectionMeta

from typing import List

import numpy as np
import cv2
import torch


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
                crop = image[int(box[2]):int(box[3]), int(box[0]):int(box[1])]
            )
            for box in row if (box[4] > self.conf_thresh) and (int(box[0]) in self.visibility_zone) and (int(box[2]) in self.visibility_zone)
        ]
        for row in predicts
    ][0]


if __name__ == "__main__":
    from config import detector_weights_path, confidence_treshold, iou_threshold, visibility_zone

    pl_d = PlantsDetector(
        model_path=detector_weights_path,
        conf_thresh=confidence_treshold,
        iou_thresh=iou_threshold,
        visibility_zone=visibility_zone
        )

    result = pl_d.predict(cv2.imread('files/test_img.jpg'))
    import pdb; pdb.set_trace()