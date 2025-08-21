from gtts import gTTS
import os

def text_to_speech(text, audio_file_path, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save(audio_file_path)

def play_audio(audio_file_path):
    if os.path.exists(audio_file_path):
        os.system(f'start {audio_file_path}')  # For Windows
    else:
        print(f"Audio file {audio_file_path} does not exist.")

def create_audio_file(text, lang='en'):
    audio_file_name = f"{text[:10].replace(' ', '_')}.mp3"  # Create a unique file name
    audio_file_path = os.path.join('audio_files', audio_file_name)
    text_to_speech(text, audio_file_path, lang)
    return audio_file_path