from dotenv import load_dotenv

load_dotenv()

import os
import click

from config import (
    video_duration,
    tower_id, backend_endpoint, 
    videos_bucket, processed_videos_bucket,
    detector_weights_path, 
    detector_confidence_treshold,
    iou_threshold, 
    classifier_weights_path,
    classifier_confidence_treshold
)

from detector.detection import PlantsDetector
from classifier.base import PytorchClassifier

from handlers.video_maker import VideoMaker
from handlers.video_recognizer import VideoRecognizer


def check_environment():
    os.environ['AWS_ACCESS_KEY_ID']
    os.environ['AWS_SECRET_ACCESS_KEY']
    os.environ['VIDEOS_BUCKET']
    os.environ['PROCESSED_VIDEOS_BUCKET']


video_maker_service = VideoMaker()

detector = PlantsDetector(
    model_path=detector_weights_path,
    conf_thresh=detector_confidence_treshold,
    iou_thresh=iou_threshold,
)

deffect_classifier = PytorchClassifier(
    model_path=classifier_weights_path,
    conf_thresh=classifier_confidence_treshold,
)

video_recognizer_service = VideoRecognizer(
    tower_id=tower_id,
    endpoint=backend_endpoint,
    raw_videos_bucket=videos_bucket,
    processed_videos_bucket=processed_videos_bucket,
    detector=detector,
    classifier=deffect_classifier
    )

@click.group()
def cli():
    pass

@cli.command()
def run_app():
    video_path = video_maker_service.record()
    video_recognizer_service.handle(video_path)


@cli.command()
@click.option('--video_path')
def run_video(video_path):
    video_recognizer_service.handle(video_path)


if __name__ == '__main__':
    check_environment()
    cli()
