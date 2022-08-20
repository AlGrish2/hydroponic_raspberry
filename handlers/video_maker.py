class VideoMaker:
    def __init__(self, save_path: str, duration: int):
        """ Service for init videowriting process

        Args:
            save_path (str): absolute
            duration (int): duration in seconds
        """
        self.save_path = save_path
        self.duration = duration

    def record(self) -> str:
        """ create and save the record

        Returns:
            str: absolute path/to/record
        """
        pass


class DummyVideoMaker(VideoMaker):
    def record(self) -> str:
        filepath = f"{self.save_path}/test-1.m4v"
        print(f"Created record: {filepath} with duration: {self.duration}seconds")
        return filepath
