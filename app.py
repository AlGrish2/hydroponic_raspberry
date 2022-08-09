import click

from config import video_duration
from handlers.video_maker import VideoMaker
from handlers.video_recognizer import VideoRecognizer

video_maker = VideoMaker('', video_duration)
video_recognizer = VideoRecognizer('', '')

@click.group()
def cli():
    pass

@cli.command()
def run_app():
    video_path = video_maker.record()
    recognized_video_path, recognition_statistics = video_recognizer.handle(video_path)


@cli.command()
@click.option('--video_path')
def run_video(video_path):
    recognized_video_path, recognition_statistics = video_recognizer.handle(video_path)


if __name__ == '__main__':
    cli()
