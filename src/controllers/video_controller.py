import logging
import os

from src.services import video_service, audio_service
from src.adapters import audio_clip, directory_adapter
from moviepy import editor

logger = logging.getLogger("delete-spaces-videos")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def _generate_audio_file(video_clip: editor.VideoFileClip, path_output: str, filename: str):
    audio = video_clip.audio

    base_output_dir = os.path.dirname(path_output)
    output_dir = os.path.join(base_output_dir, 'outputs')

    os.makedirs(output_dir, exist_ok=True)
    filename_output = os.path.join(output_dir, f"{filename}-raw-temp-audio.wav")

    audio.write_audiofile(filename_output)
    return filename_output


def _process_video(video_clip: editor.VideoFileClip, path_output: str):
    audio_file = _generate_audio_file(video_clip, path_output, video_clip.filename)
    audio_instance = audio_clip.AudioClip(audio_file)
    audio = audio_service.AudioService(audio_instance)
    audio.adjust_audio(19.8)

    silence_intervals = audio.get_silence_intervals(silence_thresh=-50, min_silence_len=1000)
    non_silent_audio = audio.remove_silence(silence_intervals)

    output_file = os.path.join(path_output, f"{video_clip.filename}-raw-temp-temp_audio_no_silence.wav")

    non_silent_audio.export(output_file, format="wav")
    new_audio_clip = editor.AudioFileClip(output_file)

    video = video_service.VideoService(video_clip)
    video_with_no_silence: editor.VideoClip = video.remove_silence_from_video(silence_intervals)
    video_with_new_audio = video_with_no_silence.set_audio(new_audio_clip)

    output_video = os.path.join(path_output, f"{video_clip.filename}-output_video_no_silence.mkv")
    video_with_new_audio.write_videofile(output_video, codec="libx264", audio_codec="aac")
    print(f"Video con audio modificado guardado en: {output_video}")


class VideoController:
    def __init__(self):
        self.adapter = directory_adapter.DirectoryAdapter()
        self.video_files = self.adapter.get_files()

    def process_videos(self):
        logger.info("Inicio de procesamiento de videos")
        output_dir = os.path.join(self.adapter.get_folder(), "outputs")
        for video_file in self.video_files:
            logger.info(f"Procesando video {video_file}")
            _process_video(editor.VideoFileClip(video_file), output_dir)
