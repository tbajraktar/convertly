from fastapi import FastAPI, UploadFile, File, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
from PIL import Image
import io
import os
app = FastAPI()

# Pre-load the session with lightweight model (u2netp) for low-memory environments
# This reduces RAM usage significantly, making it fit in Render's Free Tier (512MB)
print("Loading AI model (u2netp)...")
session = new_session("u2netp")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the 'frontend' directory
# This allows you to access the website at http://localhost:8000/
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

@app.get("/api/health")
async def health_check():
    return {"status": "online", "model": "u2netp"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    try:
        input_image = Image.open(file.file)
        print("Image opened successfully")
        
        # Use the pre-loaded session
        output_image = remove(input_image, session=session)
        print("Background removed successfully")
        
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return Response(content=img_byte_arr, media_type="image/png")
    except Exception as e:
        print(f"Error processing image: {e}")
        return Response(content=f"Error: {str(e)}", status_code=500)
