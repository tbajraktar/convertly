import os
# AGGRESSIVE MEMORY OPTIMIZATION FOR RENDER (512MB)
# These MUST be set before importing rembg/onnxruntime
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["ORT_LOGGING_LEVEL"] = "3" # Reduce onnxruntime logging memory

import io
import gc
from fastapi import FastAPI, UploadFile, File, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
from PIL import Image

app = FastAPI()

# Pre-load the session with lightweight model (u2netp) for low-memory environments
print("Loading AI model (u2netp)...")
session = new_session("u2netp")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "online", "model": "u2netp"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    try:
        input_image = Image.open(file.file)
        
        # RESIZE IF TOO LARGE (Max 1200px)
        # This is the most effective way to prevent OOM
        max_size = 1200
        if max(input_image.size) > max_size:
            print(f"Resizing image from {input_image.size} to fit {max_size}px")
            input_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        print("Processing image...")
        # Use the pre-loaded session
        output_image = remove(input_image, session=session)
        print("Background removed successfully")
        
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        result_data = img_byte_arr.getvalue()
        
        # Explicitly clean up memory
        del input_image
        del output_image
        gc.collect()
        
        return Response(content=result_data, media_type="image/png")
    except Exception as e:
        gc.collect()
        print(f"Error processing image: {e}")
        return Response(content=f"Error: {str(e)}", status_code=500)

# Serve static files from the 'frontend' directory
# This must be the LAST thing in the file so it doesn't block API routes
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
