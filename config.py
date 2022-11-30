import os


tower_id = 1
backend_endpoint = 'http://3.71.48.28:8050/post_record'

video_duration = 60

# models config
detector_weights_path = './detector/best.pt'
detector_confidence_treshold = 0.1
iou_threshold = 0.25
visibility_zone = (0, 1920) # x_start, x_end to crop only center

classifier_weights_path = './classifier/jit_model.pt'
classifier_confidence_treshold = 0.5

# s3 config
videos_bucket: str = os.environ.get('VIDEOS_BUCKET', None)
processed_videos_bucket: str = os.environ.get('PROCESSED_VIDEOS_BUCKET', None)