from src.adapters import audio_clip
from src.infrastructure import pydub_helper

class AudioService:
    def __init__(self, audio: audio_clip.AudioClip):
        self.audio_clip = audio

    def adjust_audio(self, decibeles: int | float):
        self.audio_clip.adjust_volume(decibeles)

    def get_silence_intervals(self, silence_thresh, min_silence_len):
        return pydub_helper.detect_silence(self.audio_clip.audio_segment, silence_thresh, min_silence_len)

    def remove_silence(self, silence_intervals):
        return pydub_helper.remove_silence(self.audio_clip.audio_segment, silence_intervals)
