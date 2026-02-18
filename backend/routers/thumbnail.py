from fastapi import APIRouter, Form, UploadFile, File, Response
import requests
import io
import os
import random
import logging
import textwrap
from urllib.parse import quote
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont

# Configure logging
logging.basicConfig(filename='thumbnail_debug.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

def create_text_thumbnail(text):
    """Generate a fallback image with text if AI fails."""
    try:
        width, height = 1280, 720
        # Create gradient-like background (dark subtle)
        img = Image.new('RGB', (width, height), color=(20, 20, 30))
        d = ImageDraw.Draw(img)
        
        # Draw some random shapes for "style"
        for _ in range(10):
            x0 = random.randint(0, width)
            y0 = random.randint(0, height)
            x1 = x0 + random.randint(50, 400)
            y1 = y0 + random.randint(50, 400)
            color = (random.randint(30, 80), random.randint(30, 80), random.randint(50, 100))
            d.rectangle([x0, y0, x1, y1], fill=color, outline=None)

        # Basic font handling
        try:
            # Try to load a standard font
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            # Fallback to default
            font = ImageFont.load_default()

        # Wrap text
        margin = 100
        offset = 200
        wrapped_text = textwrap.wrap(text, width=30)
        
        # Draw text
        for line in wrapped_text:
            # Simple centering (approximate)
            d.text((margin, offset), line, font=font, fill=(255, 255, 255))
            offset += 80
            
        # Draw "Generation Failed - Fallback" label
        d.text((margin, height - 100), "AI Unavailable - Text Placeholder", fill=(200, 200, 200))

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        return img_byte_arr.getvalue()
    except Exception as e:
        print(f"Fallback Creation Failed: {e}")
        return None

@router.post("/api/generate-thumbnail")
async def generate_thumbnail(prompt: str = Form(...), image: UploadFile = File(None)):
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    seed = random.randint(0, 1000000)
    
    print(f"Generating thumbnail for prompt: {prompt}")
    logging.info(f"Generating thumbnail for prompt: {prompt}")
    
    # 1. OPTIONAL: GEMINI VISION ANALYSIS
    enhanced_description = ""
    if image and api_key:
        try:
            print("Analyzing reference image with Gemini Vision...")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            image_content = await image.read()
            await image.seek(0)
            pil_image = Image.open(io.BytesIO(image_content))
            
            vision_response = model.generate_content([
                "Describe the visual style, composition, and key elements of this image in detail to help recreate a similar vibe. Keep it concise.",
                pil_image
            ])
            enhanced_description = vision_response.text
            print(f"Vision Analysis: {enhanced_description[:100]}...")
            logging.info(f"Vision Analysis: {enhanced_description[:100]}...")
        except Exception as e:
            print(f"Gemini Vision Error: {e}")
            logging.error(f"Gemini Vision Error: {e}")

    # 2. COMBINE PROMPTS
    full_prompt = f"{prompt}. {enhanced_description}" if enhanced_description else prompt
    final_prompt = f"YouTube thumbnail, {full_prompt}, high quality, 4k, vibrant colors, catchy, viral style"

    # 3. OPTIMIZE PROMPT WITH GEMINI
    optimized_prompt = final_prompt
    if api_key:
        print("Optimizing prompt with Gemini...")
        genai.configure(api_key=api_key)
        model_names = ['gemini-1.5-flash', 'gemini-1.0-pro', 'gemini-pro']
        for m_name in model_names:
            try:
                print(f"Trying Gemini model: {m_name}")
                model = genai.GenerativeModel(m_name)
                response = model.generate_content(
                    f"Create a concise, safe, high-quality AI image generation prompt for a YouTube thumbnail about: {final_prompt}. Keep it under 200 characters, no NSFW, no violence."
                )
                if response.text:
                    optimized_prompt = response.text.replace("\n", " ").strip()
                    print(f"Optimized Prompt ({m_name}): {optimized_prompt}")
                    logging.info(f"Optimized Prompt ({m_name}): {optimized_prompt}")
                    break 
            except Exception as e:
                print(f"Model {m_name} failed: {e}")

    # Aggressive truncation
    safe_prompt = optimized_prompt[:450]
    encoded_prompt = quote(safe_prompt)
    
    # URL Builder
    def get_pollinations_url(model_name=None, prompt_text=None):
        base = f"https://image.pollinations.ai/prompt/{prompt_text}?width=1280&height=720&nologo=true&seed={seed}"
        if model_name:
            base += f"&model={model_name}"
        return base

    # Re-adding User-Agent as removing it might have caused issues for Lexica/Pollinations
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Try FLUX first
    try:
        url = get_pollinations_url("flux", encoded_prompt)
        print(f"Trying Pollinations (Flux): {url}")
        logging.info(f"Requesting URL: {url}")
        
        response = requests.get(url, headers=headers, timeout=60)
        
        if response.status_code == 200:
            return Response(content=response.content, media_type="image/jpeg")
        
        error_msg = f"Flux Failed ({response.status_code})"
        print(error_msg)
        logging.error(error_msg)
        
        # Retry with TURBO
        print("Retrying with Turbo...")
        url = get_pollinations_url("turbo", encoded_prompt)
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return Response(content=response.content, media_type="image/jpeg")
            
        print(f"Turbo Failed ({response.status_code})")
        logging.error(f"Turbo Failed ({response.status_code})")
            
        # Retry with GENERIC
        print("Retrying with Generic/Default model...")
        url = get_pollinations_url(None, encoded_prompt)
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return Response(content=response.content, media_type="image/jpeg")

        print(f"Generic Failed ({response.status_code})")
        logging.error(f"Generic Failed ({response.status_code})")

        # 5. FINAL FALLBACK: LEXICA.ART SEARCH
        print("Generation APIs failed. Switching to Lexica Search...")
        logging.info("Switching to Lexica Search...")
        
        search_term = quote(prompt[:100])
        lexica_url = f"https://lexica.art/api/v1/search?q={search_term}"
        
        print(f"Searching Lexica: {lexica_url}")
        logging.info(f"Searching Lexica: {lexica_url}")
        
        response = requests.get(lexica_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data and "images" in data and len(data["images"]) > 0:
                image_url = data["images"][0]["src"]
                print(f"Found Lexica Image: {image_url}")
                logging.info(f"Found Lexica Image: {image_url}")
                
                img_response = requests.get(image_url, headers=headers, timeout=30)
                if img_response.status_code == 200:
                    return Response(content=img_response.content, media_type="image/jpeg")
            else:
                print("Lexica returned 0 results.")
                logging.warning("Lexica returned 0 results.")
        else:
             print(f"Lexica Failed ({response.status_code})")
             logging.error(f"Lexica Failed ({response.status_code})")

        # 6. ULTIMATE FALLBACK: TEXT THUMBNAIL
        print("All APIs failed. Generating Text Thumbnail...")
        logging.info("Generating Text Thumbnail...")
        fallback_img_bytes = create_text_thumbnail(prompt)
        if fallback_img_bytes:
            return Response(content=fallback_img_bytes, media_type="image/jpeg")
        
        return Response(f"System Overload. Please try again.", status_code=502)

    except Exception as e:
        print(f"Thumbnail Generation Error: {e}")
        logging.error(f"Thumbnail Generation Error: {e}")
        # Try one last time to generate text thumbnail on exception
        fallback_img_bytes = create_text_thumbnail(prompt)
        if fallback_img_bytes:
            return Response(content=fallback_img_bytes, media_type="image/jpeg")
        return Response(f"System Error: {str(e)}", status_code=500)
