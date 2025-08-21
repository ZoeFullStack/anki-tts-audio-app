import os
import requests
import random
import random
from config import TTS_SERVICE_URLS, TTS_PARAMS, AUDIO_FORMAT
from urllib.parse import urlencode

def text_to_speech(text, audio_file_path):
    """
    Fetch audio from the first available TTS service URL using TTS_PARAMS.
    """
    params = TTS_PARAMS.copy()

    # If voiceName is a comma-separated list, pick one at random
    voice_names = str(params.get('voiceName', '')).split(',')

    if len(voice_names) > 1:
        params['voiceName'] = random.choice([v.strip() for v in voice_names if v.strip()])
    params['text'] = text
    # params['format'] = AUDIO_FORMAT
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    for url in TTS_SERVICE_URLS:
        # Ensure the URL ends with /api/aiyue
        if not url.rstrip('/').endswith('api/aiyue'):
            api_url = url.rstrip('/') + '/api/aiyue'
        else:
            api_url = url.rstrip('/')
        # Manually build the full URL with query params
        full_url = f"{api_url}?{urlencode(params)}"
        print("[TTS] DEBUG: The exact request being sent:")
        print("URL:", full_url)
        print("Headers:", headers)
        try:
            response = requests.get(full_url, headers=headers, timeout=15)
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'audio' in content_type:
                    print(f"Received audio content, saving to {audio_file_path}")
                    with open(audio_file_path, 'wb') as f:
                        f.write(response.content)
                    return True
                else:
                    print(f"TTS service at {api_url} did not return audio. Content-Type: {content_type}")
                    print(f"Response content: {response.content[:200]}")
            else:
                print(f"TTS service at {api_url} returned status code {response.status_code}")
                print(f"Response content: {response.content[:200]}")
        except Exception as e:
            print(f"TTS service failed at {api_url}: {e}")
    print("All TTS services failed.")
    return False

def play_audio(audio_file_path):
    if os.path.exists(audio_file_path):
        os.system(f'start {audio_file_path}')  # For Windows
    else:
        print(f"Audio file {audio_file_path} does not exist.")

def create_audio_file(text):
    audio_file_name = f"{text[:10].replace(' ', '_')}.mp3"  # Create a unique file name
    audio_file_path = os.path.join('audio_files', audio_file_name)
    text_to_speech(text, audio_file_path)
    return audio_file_path