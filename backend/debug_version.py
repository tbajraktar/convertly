from youtube_transcript_api import YouTubeTranscriptApi
import youtube_transcript_api
import sys

print(f"Python: {sys.version}")
print(f"Library File: {youtube_transcript_api.__file__}")
print(f"Dir(YouTubeTranscriptApi): {dir(YouTubeTranscriptApi)}")
try:
    print(f"Version: {youtube_transcript_api.__version__}")
except:
    print("No version attribute")
