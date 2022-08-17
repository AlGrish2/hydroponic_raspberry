import os


video_duration = 60
fps = 10
x_start = 238
x_end = 538
confidence_treshold = 0.5

# s3 config
videos_bucket: str = os.environ.get('VIDEOS_BUCKET', None)
processed_videos_bucket: str = os.environ.get('PROCESSED_VIDEOS_BUCKET', None)