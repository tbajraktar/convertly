from youtube_transcript_api import YouTubeTranscriptApi
import inspect

print(f"Type: {type(YouTubeTranscriptApi)}")
try:
    print("Testing instantiation...")
    api = YouTubeTranscriptApi()
    print(f"Instance created: {api}")
    t = api.get_transcript("_uQrJ0TkZlc")
    print(f"Instance fetch result len: {len(t)}")
except Exception as e:
    print(f"Instantiation/Instance fetch error: {e}")

try:
    print("Testing list as instance method...")
    api = YouTubeTranscriptApi()
    t_list = api.list_transcripts("_uQrJ0TkZlc")
    print(f"list_transcripts result: {t_list}")
except Exception as e:
    print(f"list_transcripts instance error: {e}")




print("-" * 20)
print("Dir:")
print(dir(YouTubeTranscriptApi))
