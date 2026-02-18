import os
import zipfile
import io
import asyncio
from bs4 import BeautifulSoup
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import urljoin, urlparse

async def clone_site(url: str):
    # Run synchronous requests in a thread to verify it doesn't block
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _clone_site_sync, url)

def _clone_site_sync(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
    except Exception as e:
         raise Exception(f"Failed to fetch page: {str(e)}")

    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    
    # Get Title
    # Get Title and Sanitize
    raw_title = soup.title.string if soup.title and soup.title.string else "cloned_site"
    title = "".join([c for c in raw_title if c.isalnum() or c in (' ', '-', '_')]).strip()
    if not title:
        title = "cloned_site"
    
    # Get Favicon
    favicon_url = None
    icon_link = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
    if icon_link:
        href = icon_link.get("href")
        if href:
            favicon_url = urljoin(url, href)
            
    # Remove Scripts & Trackers (Clean Clone)
    for tag in soup(["script", "iframe", "object", "embed", "noscript"]):
        tag.decompose()

    # Download CSS
    css_files = {}
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href")
        if href:
            full_css_url = urljoin(url, href)
            try:
                css_resp = requests.get(full_css_url, headers=headers, timeout=5, verify=False)
                if css_resp.status_code == 200:
                    filename = os.path.basename(urlparse(full_css_url).path)
                    if not filename or not filename.endswith('.css'):
                        filename = f"style_{len(css_files)}.css"
                    
                    # Dedup filenames
                    while filename in css_files:
                         filename = f"_{filename}"

                    css_files[filename] = css_resp.content
                    link['href'] = filename
            except:
                pass 

    # Handle Images (Optional: could download them too, but for now we keep absolute links or basic relative)
    # For a purely "structural" clone, we usually leave images as absolute OR download them. 
    # Let's fix relative image links to be absolute so they don't break.
    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            img['src'] = urljoin(url, src)

    # Create Zip
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr("index.html", str(soup.prettify()))
        
        for fname, content in css_files.items():
            zip_file.writestr(fname, content)
    
    zip_buffer.seek(0)
    return zip_buffer, title, favicon_url
