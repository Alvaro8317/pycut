from typing import Any
from abc import ABC, abstractmethod

class AudioClip(ABC):
    @abstractmethod
    def __init__(self, audio_segment: Any) -> None: ...

    @abstractmethod
    def adjust_volume(self, decibeles: int) -> None: ...

    @staticmethod
    @abstractmethod
    def get_db_per_second(audio_segment: Any) -> float: ...

    def save(self, file_path: str) -> None: ...
