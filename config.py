import os


tower_id = 1
backend_endpoint = 'http://localhost:8050/post_record'

video_duration = 60
fps = 10
x_start = 100
x_end = 900

# models config
detector_weights_path = './detector/best.pt'
confidence_treshold = 0.5
iou_threshold = 0.5
visibility_zone = (300, 700) # x_start, x_end to crop only center

# s3 config
videos_bucket: str = os.environ.get('VIDEOS_BUCKET', None)
processed_videos_bucket: str = os.environ.get('PROCESSED_VIDEOS_BUCKET', None)