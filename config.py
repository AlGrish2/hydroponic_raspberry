import os


tower_id = 1
backend_endpoint = 'http://192.168.0.247:8050/post_record'

video_duration = 60

# models config
detector_weights_path = './detector/best.pt'
detector_confidence_treshold = 0.5
iou_threshold = 0.5
visibility_zone = (0, 900) # x_start, x_end to crop only center

classifier_weights_path = './classifier/jit_model.pt'
classifier_confidence_treshold = 0.5

# s3 config
videos_bucket: str = os.environ.get('VIDEOS_BUCKET', None)
processed_videos_bucket: str = os.environ.get('PROCESSED_VIDEOS_BUCKET', None)