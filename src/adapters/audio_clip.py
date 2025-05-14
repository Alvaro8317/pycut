from src.domain import audio_ports
import pydub

class AudioClip(audio_ports.AudioClip):
    def __init__(self, audio_segment: pydub.AudioSegment | str):
        self.audio_segment = audio_segment
        if isinstance(audio_segment, str):
            self.audio_segment = pydub.AudioSegment.from_wav(audio_segment)

    def adjust_volume(self, decibeles: int | float):
        self.audio_segment = self.audio_segment + decibeles

    @staticmethod
    def get_db_per_second(audio_segment: pydub.AudioSegment):
        db_per_second = []
        duration_ms = len(audio_segment)

        for i in range(0, duration_ms, 1000):
            segment = audio_segment[i:i+1000]
            db = segment.dBFS
            db_per_second.append(db)

        return db_per_second

    def save(self, file_path):
        self.audio_segment.export(file_path, format="wav")
