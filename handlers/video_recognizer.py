import os
import cv2
from tqdm import trange


class VideoRecognizer:

    def __init__(self, detector_path: str, classifier_path: str):
        self.detector_path = detector_path
        self.classifier_path = classifier_path

    def draw_predictions(self, frame):
        return frame
        
    def process_frame(self, frame):
        return []

    def process_video(self, video_path):
        capture = cv2.VideoCapture(video_path)
        length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fps = 10
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')

        output_path = f'processed/{os.path.basename(video_path)}'
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        all_recognitions = []

        for _ in trange(length, desc='Processing video...'):
            ret, frame = capture.read()
            if frame is None:
                break
            new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            frame_recognitions = self.process_frame(new_frame)
            
            all_recognitions.append(frame_recognitions)
            new_frame = self.draw_predictions(new_frame, frame_recognitions)
            
            writer.write(cv2.cvtColor(new_frame, cv2.COLOR_RGB2BGR))

        writer.release()     
        capture.release()
        return output_path, all_recognitions

    def post_results(self,  recognitions):
        pass

    def upload_videos(self, raw_video_path, processed_video_path):
        return '', ''

    def get_sensor_info(self):
        pass

    def upload_result(self):
        pass

    def clear(self):
        pass

    def handle(self, video_path: str):
        processed_video_path, recognitions = self.process_video(video_path)
        raw_video_url, processed_video_url = self.upload_videos(video_path, processed_video_path)
        sensor_info = self.get_sensor_info()
        self.upload_result(raw_video_url, processed_video_url, recognitions, sensor_info)
        self.clear()

