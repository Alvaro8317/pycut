from moviepy import editor

def extract_audio_from_video(video_file: str):
    video = editor.VideoFileClip(video_file)
    audio = video.audio
    audio_file = "temp_audio.wav"
    audio.write_audiofile(audio_file)
    return audio_file

def remove_silence_from_video(video_clip, silence_intervals) -> editor.CompositeVideoClip:
    non_silent_video: list = []
    last_end: int = 0
    for start, end in silence_intervals:
        if start > last_end:
            non_silent_video.append(video_clip.subclip(last_end, start))
        last_end = end

    if last_end < video_clip.duration:
        non_silent_video.append(video_clip.subclip(last_end, video_clip.duration))

    final_video = editor.concatenate_videoclips(non_silent_video, method="compose")
    return final_video
