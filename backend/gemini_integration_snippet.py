@app.post("/api/yt-summary")
async def yt_summary(item: YouTubeURL):
    from youtube_transcript_api import YouTubeTranscriptApi
    import google.generativeai as genai
    from dotenv import load_dotenv
    
    # Load Environment Variables
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    print(f"YT Summary: Received {item.url}")
    
    try:
        # Dictionary of video IDs (same extraction logic)
        video_id = ""
        if "v=" in item.url:
            video_id = item.url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in item.url:
            video_id = item.url.split("youtu.be/")[1].split("?")[0]
        elif "/shorts/" in item.url:
            video_id = item.url.split("/shorts/")[1].split("?")[0]
            
        if not video_id:
            return Response(content='{"error": "Invalid YouTube URL"}', status_code=400, media_type="application/json")

        # Fetch Transcript
        try:
             transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
             try:
                transcript = transcript_list.find_transcript(['en']).fetch()
             except:
                for t in transcript_list:
                    transcript = t.fetch()
                    break
        except Exception as e:
             # Fallback: maybe no transcript
             print(f"Transcript error: {e}")
             return {"summary": "Could not retrieve transcript. Video might not have captions."}

        # Combine text
        full_text = " ".join([t['text'] for t in transcript])
        
        # GEMINI SUMMARY
        if api_key:
            try:
                print("Using Gemini API...")
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""You are a helpful assistant. Summarize the following YouTube video transcript in a concise, bulleted format. Capture the main points and any actionable insights.
                
                Transcript:
                {full_text[:30000]} 
                """ 
                # Limit to ~30k chars to be safe for free tier, though 1.5 Flash has huge context.
                
                response = model.generate_content(prompt)
                return {"summary": response.text}
            except Exception as e:
                print(f"Gemini Error: {e}")
                return {"summary": f"Gemini API Error: {str(e)}"}
        else:
             # MOCK FALLBACK
             mock_summary = f"⚠️ **Mock AI Summary (No API Key Provided)**\n\nHere is a preview of the transcript:\n\n{full_text[:500]}...\n\n(To get real AI summaries, please provide a Gemini API Key in your .env file.)"
             return {"summary": mock_summary}

    except Exception as e:
        print(f"YT Summary Error: {e}")
        return Response(content=f'{{"error": "{str(e)}"}}', status_code=500, media_type="application/json")
