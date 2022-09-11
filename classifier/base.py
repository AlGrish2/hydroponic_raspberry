from dataclasses import dataclass
from typing import Protocol

import cv2
from PIL import Image
import numpy as np
import torch
import torchvision.transforms as T


from detector.base import DetectionMeta

@dataclass
class ClassificationMeta:
    nutrient_surplus: float
    magnesium: float
    phosphate: float
    healthy: float
    phosphorous: float
    nitrates: float
    potassium: float
    nitrogen: float
    calcium: float
    sulfur: float


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


class PytorchClassifier:
    def __init__(self, model_path: str, conf_thresh):
        self.conf_thresh = conf_thresh
        self.model = self._load_model(model_path)
    
    def _load_model(self, model_path):
        return torch.load(model_path) 

    def _preprocess_image(self, image: np.ndarray) -> torch.Tensor:
        image = Image.fromarray(image)
        imagenet_stats = ([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]) 
        transform = T.Compose([T.Resize(224),
                            T.ToTensor(),
                            T.Normalize(*imagenet_stats)])
        image = transform(image)
        image = image.unsqueeze(0)  # torch.Size([1, 3, 224, 224]
        return image 

    def predict(self, image: np.ndarray) -> ClassificationMeta:
        image = self._preprocess_image(image)
        with torch.no_grad():
            prediction = self.model(image)[0]  
        return ClassificationMeta(*prediction)
