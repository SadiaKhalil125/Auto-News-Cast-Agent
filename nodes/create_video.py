from elevenlabs import ElevenLabs, play, save
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ColorClip
import uuid
from nodes.newsstate import NewsState
import os
from moviepy.config import change_settings
# Set path to ImageMagick convert executable
change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.2-Q16-HDRI\\magick.exe"})
# Set your API key

client = ElevenLabs(api_key="your-elevenlabs-api-key-here")  # Replace with your actual ElevenLabs API key

def create_video_with_elevenlabs(state: NewsState):
    unique_id = uuid.uuid4().hex[:8]
    audio_filename = f"audio_{unique_id}.mp3"
    video_filename = f"video_{unique_id}.mp4"

    # Step 1: Generate audio from ElevenLabs
    audio = client.text_to_speech.convert(
    text=state['script'],
    voice_id="Xb7hH8MSUJpSbSDYk0k2",  # or other voice name / ID
    model_id="eleven_multilingual_v2"  # or "eleven_turbo_v2"
    )
   
    save(audio, audio_filename)

    # Step 2: Create video (same as before)
    video_size = (960, 720)
    background = ColorClip(size=video_size, color=(250, 240, 230), duration=10)

    text_clip = TextClip(
        state['script'],
        fontsize=40,
        color='black',
        size=video_size,
        method='caption',
        align='center'
    ).set_duration(10).set_position('center')

    audio_clip = AudioFileClip(audio_filename)
    final = CompositeVideoClip([background, text_clip]).set_audio(audio_clip)
    final.write_videofile(video_filename, fps=24)
    return {'video_path': video_filename, 'audio_path': audio_filename}
    
