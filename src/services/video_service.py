from src.infrastructure import moviepy_helper

class VideoService:
    def __init__(self, video_clip):
        self.video_clip = video_clip

    def remove_silence_from_video(self, silence_intervals):
        return moviepy_helper.remove_silence_from_video(self.video_clip, silence_intervals)
