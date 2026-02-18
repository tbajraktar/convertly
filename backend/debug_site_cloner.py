import asyncio
import os
import sys

# Add backend to path so we can import site_cloner
sys.path.append(os.getcwd())

from backend.site_cloner import clone_site

async def test_cloning():
    url = "https://example.com"
    print(f"Testing Site Cloner with URL: {url}")
    
    try:
        print("Starting clone process...")
        zip_buffer, title, favicon = await clone_site(url)
        print("✅ Clone Successful!")
        print(f"Title: {title}")
        print(f"Favicon: {favicon}")
        print(f"Zip Size: {len(zip_buffer.getvalue())} bytes")
    except Exception as e:
        print("❌ Clone Failed!")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_cloning())
