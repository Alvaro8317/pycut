import pydub
from pydub import silence

def detect_silence(audio_segment: pydub.AudioSegment, silence_thresh: int = -50, min_silence_len: int = 1000):
    silence_list = []
    chunks = silence.detect_silence(audio_segment=audio_segment, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    for start, end in chunks:
        silence_list.append((start / 1000.0, end / 1000.0))  # Convertir a segundos
    return silence_list

def remove_silence(audio_segment: pydub.AudioSegment, silence_intervals: list) -> pydub.AudioSegment:
    non_silent_audio: list = []
    last_end: int = 0
    for start, end in silence_intervals:
        if start > last_end:
            non_silent_audio.append(audio_segment[last_end * 1000:start * 1000])
        last_end = end

    if last_end < len(audio_segment) / 1000.0:
        non_silent_audio.append(audio_segment[last_end * 1000:])

    final_audio = non_silent_audio[0]
    for segment in non_silent_audio[1:]:
        final_audio += segment
    return final_audio
