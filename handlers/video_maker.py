from datetime import datetime
import time
import serial
import cv2


class VideoMaker:
    def record(self) -> str:
        """ create and save the record

        Returns:
            str: absolute path/to/record
        """
        video_path = f'{datetime.now()}.mp4'.replace(' ', '_')
        
        width = 1920 #int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = 1080 #int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = 1 #capture.get(cv2.CAP_PROP_FPS)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(video_path, fourcc, fps, (height, width))

        # serial1 = serial.Serial('/dev/ttyACM0', 9600)
        # serial1.flush()
        for i in range(8):
            stepstomove = 1
            stepstomove = str(stepstomove)
            stepstomoveencode = stepstomove.encode()
            # serial1.write(stepstomoveencode)
            time.sleep(3)
            capture = cv2.VideoCapture(0)
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            ret, frame = capture.read()
            frame = cv2.rotate(frame, rotateCode=2)
            writer.write(frame)
            capture.release()
        
        stepstomove = 2
        stepstomove = str(stepstomove)
        stepstomoveencode = stepstomove.encode()
        for i in range(8):
            serial1.write(stepstomoveencode)
            time.sleep(2)

        stepstomove = 0
        stepstomove = str(stepstomove)
        stepstomoveencode = stepstomove.encode()
        serial1.write(stepstomoveencode)

        writer.release()
        
        return video_path


class DummyVideoMaker(VideoMaker):
    def record(self) -> str:
        filepath = f"{self.save_path}/test-1.m4v"
        print(f"Created record: {filepath} with duration: {self.duration}seconds")
        return filepath
