import os
from typing import List, Tuple
from datetime import datetime

import cv2
import numpy as np
import requests

from detector.base import DetectionMeta, Detector
from classifier.base import ClassificationMeta, Classifier

from handlers.models import SensorsSchema, RequestSchema, AgregatedRecognitionsSchema

from transport.s3 import upload_file


class VideoRecognizer:
    """ Service with processing video through ML models
        Read created Video
        Create and save video with recognition results
        Get Sensors information
        Push created videofile to s3
        Post results to hydroponic_server
        Clear created videos
    """
    def __init__(
        self, 
        tower_id: int,
        endpoint: str,
        raw_videos_bucket: str,
        processed_videos_bucket: str,
        detector: Detector, 
        classifier: Classifier
        ):
        
        self.tower_id = tower_id
        self.endpoint = endpoint

        self.raw_videos_bucket = raw_videos_bucket
        self.processed_videos_bucket = processed_videos_bucket

        self.detector = detector
        self.classifier = classifier

    def draw_predictions(self, frame: np.ndarray, preds: Tuple[List[DetectionMeta], List[ClassificationMeta]]):
        for det, c_meta in zip(preds[0], preds[1]):
            # label = f"plant"
            frame = cv2.rectangle(frame, (det.x_min, det.y_min), (det.x_max, det.y_max), (0, 255, 0), 3)
            frame = cv2.putText(frame, f'size: {det.size}', (det.x_min, det.y_min), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
        import config
        frame = cv2.line(frame, (config.visibility_zone[0], 0), (config.visibility_zone[0], frame.shape[0]), (0, 255, 0), thickness=2)
        frame = cv2.line(frame, (config.visibility_zone[1], 0), (config.visibility_zone[1], frame.shape[0]), (0, 255, 0), thickness=2)
        return frame
        
    def process_frame(self, frame: np.ndarray) -> Tuple[List[DetectionMeta], List[ClassificationMeta]]:
        """ Inference detection and classification model on frame

        Args:
            frame (np.ndarray): frame from video

        Returns:
        """
        detections: List[DetectionMeta] = self.detector.predict(frame)
        classifications = []
        for det in detections:
            cls_meta: ClassificationMeta = self.classifier.predict(det.crop)
            classifications.append(cls_meta)
        return detections, classifications

    def process_video(self, video_path):
        capture = cv2.VideoCapture(video_path)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fps = capture.get(cv2.CAP_PROP_FPS)
        
        if not os.path.exists('processed/'):
            os.makedirs('processed/')
        output_path = f'processed/{os.path.basename(video_path)}.mp4'

        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        all_recognitions = []

        while capture.isOpened():
            ret, frame = capture.read()
            if frame is None:
                break
            new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_recognitions = self.process_frame(new_frame)
            new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)
            
            all_recognitions.append(frame_recognitions)
            new_frame = self.draw_predictions(new_frame, frame_recognitions)

            writer.write(new_frame)

        writer.release()
        capture.release()
        return output_path, all_recognitions

    def upload_videos(self, raw_video_path, processed_video_path):
        raw_video_s3_link = upload_file(raw_video_path, self.raw_videos_bucket)
        processed_video_s3_link = upload_file(processed_video_path, self.processed_videos_bucket)
        return raw_video_s3_link, processed_video_s3_link

    def get_sensor_info(self) -> SensorsSchema:

        try:
            from hardware_interface.raspberry_code.raspberrysensors import DataCollection
            collector = DataCollection()
            print('Сonnection to sensors')
            sensor_info = collector.get_sensor_data()
            min_wl: int = sensor_info['min_wl']
            max_wl: int = sensor_info['max_wl']
            air_temp: float = sensor_info['air_temp']
            hum: float = sensor_info['hum']
            pres: float = sensor_info['pres']
            water_temp: float = sensor_info['water_temp']
            light1: float = sensor_info['light1']
            light2: float = sensor_info['light2']
            light3: float = sensor_info['light3']
            light4: float = sensor_info['light4']
            ph: float = sensor_info['ph']
            ec: float = sensor_info['ec']
            tds: float = sensor_info['tds']
        except Exception:
            min_wl: int = 0
            max_wl: int = 1
            air_temp: float = 0.5
            hum: float = 0.5
            pres: float = 0.5
            water_temp: float = 0.5
            light1: float = 0.5
            light2: float = 0.5
            light3: float = 0.5
            light4: float = 0.5
            ph: float = 0.5
            ec: float = 0.5
            tds: float = 0.5

        sensors_schema = SensorsSchema(
            min_wl = min_wl,
            max_wl = max_wl,
            air_temp = air_temp,
            hum = hum,
            pres = pres,
            water_temp = water_temp,
            light1 = light1,
            light2 = light2,
            light3 = light3,
            light4 = light4,
            ph = ph,
            ec = ec,
            tds = tds
        )
        return sensors_schema

    def serialize(
        self,
        timestamp: datetime,
        raw_video_url: str,
        processed_video_url: str,
        agregated_info: AgregatedRecognitionsSchema,
        sensor_info: SensorsSchema
        ) -> RequestSchema:
        
        request_schema = RequestSchema(
            tower_id=self.tower_id,
            timestamp=timestamp,
            raw_video_url=raw_video_url,
            processed_video_url=processed_video_url,
            mean_size=agregated_info.mean_size,
            nutrient_surplus=agregated_info.nutrient_surplus,
            magnesium=agregated_info.magnesium,
            phosphate=agregated_info.phosphate,
            healthy=agregated_info.healthy,
            phosphorous=agregated_info.phosphorous,
            nitrates=agregated_info.nitrates,
            potassium=agregated_info.potassium,
            nitrogen=agregated_info.nitrogen,
            calcium=agregated_info.calcium,
            sulfur=agregated_info.sulfur,
            min_wl = sensor_info.min_wl,
            max_wl = sensor_info.max_wl,
            air_temp = sensor_info.air_temp,
            hum = sensor_info.hum,
            pres = sensor_info.pres,
            water_temp = sensor_info.water_temp,
            light1 = sensor_info.light1,
            light2 = sensor_info.light2,
            light3 = sensor_info.light3,
            light4 = sensor_info.light4,
            ph = sensor_info.ph,
            ec = sensor_info.ec,
            tds = sensor_info.tds
        )
        return request_schema

    def agregate_results(self, recognitions: List[Tuple[List[DetectionMeta], List[ClassificationMeta]]]) -> AgregatedRecognitionsSchema:
        """ 
        Business logic, process and agregate recognitions
        """
        # TODO Count values frome frame recognitions
        agregated_recs_schema = AgregatedRecognitionsSchema(
            mean_size=np.mean([det.size for rec in recognitions for det in rec[0]]),
            nutrient_surplus=np.mean([clf.nutrient_surplus for rec in recognitions for clf in rec[1]]),
            magnesium=np.mean([clf.magnesium for rec in recognitions for clf in rec[1]]),
            phosphate=np.mean([clf.phosphate for rec in recognitions for clf in rec[1]]),
            healthy=np.mean([clf.healthy for rec in recognitions for clf in rec[1]]),
            phosphorous=np.mean([clf.phosphorous for rec in recognitions for clf in rec[1]]),
            nitrates=np.mean([clf.nitrates for rec in recognitions for clf in rec[1]]),
            potassium=np.mean([clf.potassium for rec in recognitions for clf in rec[1]]),
            nitrogen=np.mean([clf.nitrogen for rec in recognitions for clf in rec[1]]),
            calcium=np.mean([clf.calcium for rec in recognitions for clf in rec[1]]),
            sulfur=np.mean([clf.sulfur for rec in recognitions for clf in rec[1]])
        )
        return agregated_recs_schema

    def upload_result(self, request_schema: RequestSchema):
        r = requests.post(self.endpoint, json=request_schema.dict())
        print(request_schema.dict())
        print(r)

    def clear(self, raw_video_path: str, processed_video_path: str):
        # os.remove(raw_video_path)
        os.remove(processed_video_path)
        print(f"Files: {raw_video_path}, {processed_video_path} deleted")

    def handle(self, video_path: str):
        sensor_info = self.get_sensor_info()
        timestamp = datetime.now().timestamp()
        processed_video_path, recognitions = self.process_video(video_path)
        raw_video_url, processed_video_url = self.upload_videos(video_path, processed_video_path)

        agregated_results = self.agregate_results(recognitions)

        request_schema = self.serialize(
            timestamp, 
            raw_video_url, 
            processed_video_url,
            agregated_results,
            sensor_info
        )

        self.upload_result(request_schema)
        self.clear(video_path, processed_video_path)
