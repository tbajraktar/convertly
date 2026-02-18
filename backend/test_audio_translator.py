import requests
import io

# Mock Audio File (content doesn't matter for mock transcription)
dummy_audio = io.BytesIO(b"fake audio content")
dummy_audio.name = "test_audio.mp3"

url = "http://localhost:8000/api/audio-translator"
files = {'file': ('test_audio.mp3', dummy_audio, 'audio/mpeg')}
data = {'target_lang': 'es'} # Translate to Spanish

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, files=files, data=data)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
        result = response.json()
        print("-" * 20)
        print(f"Original: {result['original_text']}")
        print("-" * 20)
        print(f"Translated (ES): {result['translated_text']}")
        print("-" * 20)
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
