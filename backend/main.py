import os
import io
import gc
import asyncio
from fastapi import FastAPI, UploadFile, File, Response, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

# EXTREME MEMORY OPTIMIZATION FOR 512MB RAM
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["ORT_LOGGING_LEVEL"] = "3"

app = FastAPI()

# Include Routers
from backend.routers import terminal, thumbnail
app.include_router(terminal.router)
app.include_router(thumbnail.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "online", "mode": "extreme-low-memory"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    
    # We must import rembg here or at the top, but the session MUST be local
    from rembg import remove, new_session
    
    try:
        # Load image
        input_image = Image.open(file.file)
        
        # AGGRESSIVE RESIZE (800px is very safe for 512MB)
        max_size = 800
        if max(input_image.size) > max_size:
            print(f"Resizing from {input_image.size} to {max_size}px")
            input_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        print("Loading AI model session...")
        # Create a fresh session for THIS request only
        # Using u2netp (smallest model)
        session = new_session("u2netp")
        
        print("Processing image...")
        output_image = remove(input_image, session=session)
        
        # Export to bytes
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        result_data = img_byte_arr.getvalue()
        
        # 🚨 THE CRITICAL PART: WIPE EVERYTHING FROM RAM IMMEDIATELY
        print("Cleaning up memory...")
        del session
        del input_image
        del output_image
        gc.collect()
        
        return Response(content=result_data, media_type="image/png")
        
    except Exception as e:
        print(f"Error: {e}")
        gc.collect()
@app.post("/api/mp3-extractor")
async def extract_mp3(file: UploadFile = File(...)):
    import tempfile
    from moviepy import VideoFileClip
    
    print(f"MP3 Extractor: Received {file.filename}")
    
    # Create temp files for input/output
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
        temp_input.write(await file.read())
        input_path = temp_input.name
        
    output_path = input_path.replace(".mp4", ".mp3")
    
    try:
        # Extract Audio
        video = VideoFileClip(input_path)
        video.audio.write_audiofile(output_path, logger=None)
        video.close()
        
        # Read the MP3
        with open(output_path, "rb") as f:
            mp3_data = f.read()
            
        print("MP3 Extractor: Success")
        return Response(content=mp3_data, media_type="audio/mpeg", headers={"Content-Disposition": f"attachment; filename={file.filename.replace('.mp4', '.mp3')}"})

    except Exception as e:
        print(f"MP3 Extractor Error: {e}")
        return Response(content=f"Error: {str(e)}", status_code=500)
        
    finally:
        # Cleanup
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)
        gc.collect()

from pydantic import BaseModel

class YouTubeURL(BaseModel):
    url: str

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
        # Extract Video ID
        video_id = ""
        if "v=" in item.url:
            video_id = item.url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in item.url:
            video_id = item.url.split("youtu.be/")[1].split("?")[0]
        elif "/shorts/" in item.url:
            video_id = item.url.split("/shorts/")[1].split("?")[0]
            
        if not video_id:
            print(f"Invalid URL format: {item.url}")
            return Response(content='{"error": "Invalid YouTube URL"}', status_code=400, media_type="application/json")

        # Fetch Transcript
        try:
             # Instance-based usage for this version of youtube_transcript_api
             yt_api = YouTubeTranscriptApi()
             
             # usage: fetch(video_id, languages=['en'])
             transcript = yt_api.fetch(video_id, languages=['en', 'en-US'])
             
        except Exception as e:
            # Fallback: try listing all and getting first
            try:
                print(f"Direct fetch failed, trying list: {e}")
                transcript_list = yt_api.list(video_id)
                for t in transcript_list:
                    transcript = t.fetch()
                    break
            except Exception as e2:
                print(f"Transcript fetch failed: {e2}")
                return {"summary": "Could not retrieve transcript. The video might not have captions enabled or they are not accessible."}

        # Combine text
        if not transcript:
            return {"summary": "No transcript available for this video."}
            
        try:
            if isinstance(transcript[0], dict):
                 full_text = " ".join([t['text'] for t in transcript])
            else:
                 full_text = " ".join([t.text for t in transcript])
        except:
            full_text = str(transcript)

        # GEMINI SUMMARY
        if api_key:
            try:
                print("Using Gemini API...")
                genai.configure(api_key=api_key)
                # 'gemini-flash-latest' points to the latest stable Flash model (likely 1.5-flash)
                # This usually has better free-tier availability than the 2.0 preview.
                model = genai.GenerativeModel('gemini-flash-latest')
                
                prompt = f"""You are a helpful assistant. Summarize the following YouTube video transcript in a concise, bulleted format. Capture the main points and any actionable insights.
                
                Transcript:
                {full_text[:30000]} 
                """
                
                response = model.generate_content(prompt)
                return {"summary": response.text}
            except Exception as e:
                print(f"Gemini Error: {e}")
                return {"summary": f"Gemini API Error: {str(e)}"}
        else:
            # MOCK A.I. SUMMARY (Since no API Key)
            mock_summary = f"⚠️ **Mock AI Summary (No API Key Provided)**\n\nHere is a preview of the transcript:\n\n{full_text[:500]}...\n\n(To get real AI summaries, please provide a Gemini API Key in your .env file.)"
            return {"summary": mock_summary}

    except Exception as e:
        print(f"YT Summary Error: {e}")
        return Response(content=f'{{"error": "{str(e)}"}}', status_code=500, media_type="application/json")

@app.post("/api/audio-translator")
async def audio_translator(file: UploadFile = File(...), target_lang: str = Form("en")):
    from deep_translator import GoogleTranslator
    import random
    
    print(f"Audio Translator: Received {file.filename} -> {target_lang}")
    
    try:
        # Save temp file for Gemini Upload
        import tempfile
        import google.generativeai as genai
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        # Save upload to temp file
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_audio:
            tmp_audio.write(await file.read())
            tmp_path = tmp_audio.name

        transcript_text = ""

        if api_key:
            try:
                print("Using Gemini for Audio Transcription...")
                genai.configure(api_key=api_key)
                
                # Upload to Gemini
                print(f"Uploading {file.filename} to Gemini...")
                audio_file = genai.upload_file(path=tmp_path, mime_type=file.content_type or "audio/mp3")
                
                # Generate Content
                # Used 'gemini-flash-latest' to match the working model from YT Summary
                model = genai.GenerativeModel('gemini-flash-latest')
                print("Generating transcription...")
                response = model.generate_content([
                    "Transcribe this audio file exactly as spoken. Return ONLY the text, no conversational filler.",
                    audio_file
                ])
                
                transcript_text = response.text
                print("Transcription success.")
                
                # Cleanup Gemini file (optional but good practice)
                # genai.delete_file(audio_file.name) 

            except Exception as e:
                print(f"Gemini Transcription Failed: {e}")
                transcript_text = f"Error during AI transcription: {str(e)}"
        else:
            # Fallback if no key
            transcript_text = "⚠️ Error: No Gemini API Key found. Please configure .env file."

        # REAL TRANSLATION
        print(f"Translating to {target_lang}...")
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated_text = translator.translate(transcript_text[:4500]) # 5k char limit for free deep_translator
        
        # Cleanup local temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        
        return {
            "original_text": transcript_text,
            "translated_text": translated_text
        }

    except Exception as e:
        print(f"Audio Translator Error: {e}")
        return Response(content=f'{{"error": "{str(e)}"}}', status_code=500, media_type="application/json")

# Site Cloner Endpoint
@app.post("/api/site-cloner")
async def site_cloner(request: Request):
    from backend.site_cloner import clone_site
    
    data = await request.json()
    url = data.get("url")
    
    if not url:
        return Response("Missing URL", status_code=400)

    try:
        zip_buffer, title, favicon = await clone_site(url)
        
        # Return as downloadable zip
        return Response(
            content=zip_buffer.getvalue(),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename={title}_cloned.zip",
                "X-Favicon-Url": favicon or ""
            }
        )
    except Exception as e:
        print(f"Clone Error: {e}")
        return Response(f"Failed to clone site: {str(e)}", status_code=500)
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
