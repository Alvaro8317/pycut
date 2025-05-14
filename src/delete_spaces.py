from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import pydub
from pydub import silence

# Función para obtener el nivel de dB promedio de cada segundo
def get_db_per_second(audio_segment: pydub.AudioSegment) -> list[float]:
    db_per_second = []
    duration_ms = len(audio_segment)

    # Dividir el audio en segundos y calcular el dB de cada uno
    for i in range(0, duration_ms, 1000):  # 1000 ms = 1 segundo
        segment = audio_segment[i:i+1000]  # Tomar 1 segundo de audio
        db = segment.dBFS  # Calcular el dB promedio para ese segundo
        db_per_second.append(db)

    return db_per_second

# Función para detectar los silencios
def detect_silence(audio: pydub.AudioSegment, silence_thresh: int = -50, min_silence_len: int = 1000) -> list[tuple[float, float]]:
    silence_list = []
    # Detectar los intervalos de silencio
    chunks = silence.detect_silence(audio_segment=audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    for start, end in chunks:
        silence_list.append((start / 1000.0, end / 1000.0))  # Convertir a segundos
    return silence_list

# Función para eliminar los silencios del audio
def remove_silence(audio_segment: pydub.AudioSegment, silence_intervals: list) -> pydub.AudioSegment:
    # Crear una lista para los segmentos de audio que no contienen silencio
    non_silent_audio = []

    last_end = 0
    for start, end in silence_intervals:
        # Añadir el segmento de audio previo al silencio
        if start > last_end:
            non_silent_audio.append(audio_segment[last_end * 1000:start * 1000])  # Convertir a milisegundos
        last_end = end

    # Añadir la última parte del audio (después del último silencio)
    if last_end < len(audio_segment) / 1000.0:
        non_silent_audio.append(audio_segment[last_end * 1000:])

    # Unir todos los segmentos no silenciosos utilizando concatenación
    final_audio = non_silent_audio[0]  # Inicializar con el primer segmento
    for segment in non_silent_audio[1:]:  # Concatenar los siguientes
        final_audio += segment

    return final_audio

# Función para cortar el video en los mismos intervalos que los silencios
def remove_silence_from_video(video_clip: VideoFileClip, silence_intervals: list) -> VideoFileClip:
    # Crear una lista para los segmentos de video que no contienen silencio
    non_silent_video = []

    last_end = 0
    for start, end in silence_intervals:
        # Añadir el segmento de video previo al silencio
        if start > last_end:
            non_silent_video.append(video_clip.subclip(last_end, start))
        last_end = end

    # Añadir la última parte del video (después del último silencio)
    if last_end < video_clip.duration:
        non_silent_video.append(video_clip.subclip(last_end, video_clip.duration))

    # Unir todos los segmentos de video no silenciosos
    final_video = concatenate_videoclips(non_silent_video, method="compose")

    return final_video

# Función para convertir el video a audio, aumentar el volumen, detectar los silencios y crear el nuevo audio y video sin silencios
def analyze_video_for_silence(video_file: str):
    # Extraer audio del video
    video = VideoFileClip(video_file)
    audio = video.audio
    audio_file = "../temp_audio.wav"
    audio.write_audiofile(audio_file)

    # Cargar el audio usando pydub
    audio_segment = pydub.AudioSegment.from_wav(audio_file)

    # Subir el volumen en 9.8 dB
    audio_segment = audio_segment + 19.8  # Esto sube el volumen en 19.8 dB

    # Obtener los dB por segundo para el análisis
    db_per_second = get_db_per_second(audio_segment)

    # Detectar los silencios
    silence_intervals = detect_silence(audio_segment)

    # Crear un nuevo audio sin los silencios
    non_silent_audio = remove_silence(audio_segment, silence_intervals)

    # Guardar el nuevo archivo de audio sin silencios
    output_audio_file = "../temp_audio_no_silence.wav"
    non_silent_audio.export(output_audio_file, format="wav")
    print(f"Nuevo audio sin los silencios guardado en: {output_audio_file}")

    # Crear el video sin los silencios
    video_with_no_silence = remove_silence_from_video(video, silence_intervals)

    # Crear un nuevo archivo de audio para el video
    new_audio_clip = AudioFileClip(output_audio_file)

    # Reemplazar el audio del video original con el nuevo audio sin silencios
    video_with_new_audio = video_with_no_silence.set_audio(new_audio_clip)

    # Guardar el video con el nuevo audio
    output_video_file = "output_video_no_silence.mkv"
    video_with_new_audio.write_videofile(output_video_file, codec="libx264", audio_codec="aac")
    print(f"Video con audio modificado guardado en: {output_video_file}")

if __name__ == "__main__":
    video_file = "../test.mkv"  # Aquí pon la ruta de tu archivo de video
    analyze_video_for_silence(video_file)
