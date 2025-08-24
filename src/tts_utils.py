from gtts import gTTS
import os
import asyncio
import subprocess
import sys

def text_to_speech(text, audio_file_path, lang='en', engine='edge', api_key=None, voice=None, 
                  aws_access_key=None, aws_secret_key=None, aws_region=None):
    """
    Convert text to speech using various TTS engines
    :param text: The text to convert to speech
    :param audio_file_path: Output audio file path
    :param lang: Language code (e.g., 'en', 'ja', 'zh-CN'), used for gTTS mode
    :param engine: TTS engine, options: 'gtts' (Google), 'edge' (free)
    :param api_key: OpenAI API key, if None tries to get from environment (OpenAI engine only)
    :param voice: Voice model, used by Edge TTS, different voices available for different engines
    :param aws_access_key: AWS access key ID (Amazon engine only - deprecated)
    :param aws_secret_key: AWS secret access key (Amazon engine only - deprecated)
    :param aws_region: AWS region, e.g., 'us-east-1' (Amazon engine only - deprecated)
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(audio_file_path)), exist_ok=True)
    
    # 1. Edge TTS Engine (free, no API key required)
    if engine.lower() == 'edge':
        try:
            # Default Japanese voice
            if voice is None:
                voice = "ja-JP-NanamiNeural"
            
            # Method 1: Use command line tool (more reliable)
            try:
                cmd = f'edge-tts --voice "{voice}" --text "{text}" --write-media "{audio_file_path}"'
                print(f"Executing command: {cmd}")
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                print(f"Successfully generated audio using Edge TTS command line: {audio_file_path}")
                return
            except subprocess.CalledProcessError as e:
                print(f"Edge TTS command line error: {e}")
                print(f"Trying Edge TTS library...")
                
            # Method 2: Use Python library
            try:
                # Dynamic import to avoid errors when library is not installed
                import importlib.util
                spec = importlib.util.find_spec('edge_tts')
                if spec:
                    edge_tts = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(edge_tts)
                    
                    # Use async function to generate speech
                    async def generate_speech():
                        communicate = edge_tts.Communicate(text, voice)
                        await communicate.save(audio_file_path)
                    
                    # Run the async function
                    asyncio.run(generate_speech())
                    print(f"Successfully generated audio using Edge TTS library: {audio_file_path}")
                    return
            except Exception as e:
                print(f"Edge TTS library error: {str(e)}")
        
        except Exception as e:
            print(f"Error using Edge TTS: {str(e)}")
            print("Falling back to gTTS...")
    
    # 2. OpenAI TTS Engine (requires API key)
    elif engine.lower() == 'openai':
        try:
            # Get API key
            if api_key is None:
                api_key = os.environ.get("OPENAI_API_KEY")
                if api_key is None or api_key == "":
                    print("No OpenAI API key found, falling back to gTTS")
                    engine = 'gtts'
                    
            if engine.lower() == 'openai':
                # Import requests library
                import requests
                
                # Default voice setting
                if voice is None:
                    voice = "alloy"  # OpenAI default voice
                
                # Set request headers and data
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": "tts-1",  # Can also use "tts-1-hd" for higher quality
                    "input": text,
                    "voice": voice,
                    "response_format": "mp3"
                }
                
                # Send request to OpenAI TTS API
                response = requests.post(
                    "https://api.openai.com/v1/audio/speech",
                    headers=headers,
                    json=data
                )
                
                # Check response
                response.raise_for_status()
                
                # Save audio file
                with open(audio_file_path, "wb") as f:
                    f.write(response.content)
                
                print(f"Successfully generated audio using OpenAI TTS: {audio_file_path}")
                return
        except Exception as e:
            print(f"Error using OpenAI TTS: {str(e)}")
            print("Falling back to gTTS...")
    
    # 3. Amazon Polly TTS Engine (requires AWS keys) - Deprecated but keeping code for reference
    elif engine.lower() == 'amazon':
        try:
            # Get AWS credentials
            if aws_access_key is None:
                aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
            if aws_secret_key is None:
                aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
            if aws_region is None:
                aws_region = os.environ.get("AWS_REGION", "us-east-1")
            
            # Check credentials
            if not aws_access_key or not aws_secret_key:
                print("AWS credentials not found, falling back to gTTS")
                engine = 'gtts'
            
            if engine.lower() == 'amazon':
                try:
                    # Dynamic import of boto3 to avoid dependency issues
                    import importlib.util
                    spec = importlib.util.find_spec('boto3')
                    if spec is None:
                        print("boto3 library not found, please run pip install boto3")
                        print("Falling back to gTTS...")
                        engine = 'gtts'
                    else:
                        boto3 = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(boto3)
                        
                        # Default Japanese female voice
                        if voice is None:
                            voice = "Mizuki"  # Japanese female voice
                        
                        # Create Polly client
                        polly_client = boto3.client(
                            'polly',
                            aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_key,
                            region_name=aws_region
                        )
                        
                        # Request speech synthesis, specifically for Japanese
                        response = polly_client.synthesize_speech(
                            Text=text,
                            OutputFormat='mp3',
                            VoiceId=voice,
                            Engine='neural',  # 'neural' provides more natural sound
                            LanguageCode='ja-JP'  # Explicitly specify Japanese
                        )
                        
                        # Save audio file
                        if "AudioStream" in response:
                            with open(audio_file_path, 'wb') as file:
                                file.write(response['AudioStream'].read())
                            print(f"Successfully generated audio using Amazon Polly: {audio_file_path}")
                            return
                except Exception as e:
                    print(f"Error using Amazon Polly: {str(e)}")
                    print("Falling back to gTTS...")
        except Exception as e:
            print(f"Amazon Polly configuration error: {str(e)}")
            print("Falling back to gTTS...")
    
    # 4. Google TTS Engine (free, but with limitations)
    # If previous engines fail or if gTTS is specified
    try:
        # Get TLD from parameters if provided, otherwise use 'com'
        tld = getattr(sys.modules.get('config'), 'GTTS_TLD', 'com') if voice is None else voice
        
        # Create gTTS object with specified language and TLD
        tts = gTTS(text=text, lang=lang, tld=tld)
        tts.save(audio_file_path)
        print(f"Successfully generated audio using Google TTS (lang={lang}, tld={tld}): {audio_file_path}")
    except Exception as e:
        print(f"Error using Google TTS: {str(e)}")
        raise Exception("All TTS engines failed")

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