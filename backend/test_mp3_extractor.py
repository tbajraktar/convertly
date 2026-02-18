import requests
import os

# Create a dummy mp4 file if it doesn't exist
dummy_mp4 = "test.mp4"
if not os.path.exists(dummy_mp4):
    with open(dummy_mp4, "wb") as f:
        f.write(b"fake mp4 content" * 100) # This won't work with moviepy but tests the endpoint flow up to conversion

# Real test needs a valid mp4, but we want to see if the import works first.
# If moviepy is installed, it will fail at "OSError: MoviePy error: the file test.mp4 could not be found or... isn't a video file"
# If moviepy is NOT installed, it will fail at "ImportError" inside the endpoint (500)

url = "http://localhost:8000/api/mp3-extractor"
files = {'file': open(dummy_mp4, 'rb')}

try:
    print("Sending request...")
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Request failed: {e}")
finally:
    if os.path.exists(dummy_mp4):
        os.remove(dummy_mp4)
