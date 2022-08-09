
from dataclasses import dataclass


@dataclass
class RecognitionStatistics:
    leaf_count: int

class VideoRecognizer:

    def __init__(self, detector_path: str, classifier_path: str):
        self.detector_path = detector_path
        self.classifier_path = classifier_path

    def handle(self, video_path: str) -> tuple[str, RecognitionStatistics]:
        pass
