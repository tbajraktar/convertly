from youtube_transcript_api import YouTubeTranscriptApi
import sys

def test_transcript(video_url):
    print(f"Testing URL: {video_url}")
    
    # Extract ID
    video_id = ""
    if "v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        video_id = video_url.split("youtu.be/")[1].split("?")[0]
    elif "/shorts/" in video_url:
        video_id = video_url.split("/shorts/")[1].split("?")[0]
        
    print(f"Video ID: {video_id}")

    try:
        # Instantiate
        yt = YouTubeTranscriptApi()
        
        # Method 1: fetch (Simple)
        print("--- Method 1: yt.fetch(['en']) ---")
        try:
             t = yt.fetch(video_id, languages=['en', 'en-US'])
             print("Success! (Length: )", len(t))
             return
        except Exception as e:
             print(f"Method 1 Failed: {e}")

        # Method 2: list (Advanced)
        print("--- Method 2: yt.list() ---")
        transcript_list = yt.list(video_id)
        
        print("Available Transcripts:")
        for transcript in transcript_list:
            print(f" - {transcript.language_code} ({transcript.language}) | Generated: {transcript.is_generated}")

        # Try to fetch ANY
        print("Fetching first available...")
        for transcript in transcript_list:
            t = transcript.fetch()
            print("Success fetching:", transcript.language_code)
            # print("Snippet:", t[0])
            break

    except Exception as e:
        print(f"FATAL ERROR: {e}")

if __name__ == "__main__":
    # Test with the Short from the screenshot (inferred or generic) and a normal video
    urls = [
        "https://www.youtube.com/shorts/XT-1_D4q6xA", # The one from the screenshot/log
        "https://www.youtube.com/watch?v=jNQXAC9IVRw" # Me at the zoo (reliable)
    ]
    
    for url in urls:
        print("\n" + "="*50)
        test_transcript(url)
