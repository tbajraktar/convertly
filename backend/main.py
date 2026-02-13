import os
# AGGRESSIVE MEMORY OPTIMIZATION FOR RENDER (512MB)
# These MUST be set before importing rembg/onnxruntime
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["ORT_LOGGING_LEVEL"] = "3"

import io
import gc
from fastapi import FastAPI, UploadFile, File, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
from PIL import Image

app = FastAPI()

# Global session variable for lazy loading
session = None

def get_session():
    global session
    if session is None:
        print("Lazy loading AI model (u2netp)...")
        session = new_session("u2netp")
    return session

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    # Only check if server is up, don't load model yet
    return {"status": "online", "model_loaded": session is not None}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    try:
        input_image = Image.open(file.file)
        
        # AGGRESSIVE RESIZE for 512MB RAM
        # 1000px is the safe limit for most images on 512MB
        max_size = 1000
        if max(input_image.size) > max_size:
            print(f"Resizing image to fit {max_size}px")
            input_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        print("Processing...")
        # Lazy load model here
        ai_session = get_session()
        output_image = remove(input_image, session=ai_session)
        
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        result_data = img_byte_arr.getvalue()
        
        # Cleanup
        del input_image
        del output_image
        gc.collect()
        
        return Response(content=result_data, media_type="image/png")
    except Exception as e:
        gc.collect()
        print(f"Error: {e}")
        return Response(content=f"Error: {str(e)}", status_code=500)

# Serve static files LAST
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
