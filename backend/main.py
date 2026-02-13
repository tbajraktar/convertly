import os
import io
import gc
import asyncio
from fastapi import FastAPI, UploadFile, File, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

# EXTREME MEMORY OPTIMIZATION FOR 512MB RAM
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["ORT_LOGGING_LEVEL"] = "3"

app = FastAPI()

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
        return Response(content=f"Error: {str(e)}", status_code=500)

# Serve static files LAST
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
