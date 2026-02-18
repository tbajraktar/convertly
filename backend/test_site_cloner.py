import asyncio
from backend.site_cloner import clone_site
import os

async def test_clone():
    url = "https://example.com"
    print(f"Testing Site Cloner with {url}...")
    
    try:
        zip_buffer, title, favicon = await clone_site(url)
        print(f"Success! Clone Title: {title}")
        print(f"Favicon: {favicon}")
        print(f"Zip Size: {len(zip_buffer.getvalue())} bytes")
        
        # Save to file for manual inspection if needed
        with open("test_clone.zip", "wb") as f:
             f.write(zip_buffer.getvalue())
        print("Saved to test_clone.zip")
        
    except Exception as e:
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_clone())
