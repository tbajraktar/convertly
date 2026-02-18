import os
from bs4 import BeautifulSoup

# Configuration for each tool
TOOLS = {
    "mp3-extractor": {
        "title": "Free MP3 Extractor - Convertly",
        "h1": 'Extract <span class="gradient-text">MP3 Audio</span>',
        "subtitle": 'Extract high-quality MP3 from MP4 videos instantly.',
        "description": "Extract high-quality MP3 audio from MP4 videos instantly. Private, fast, and free.",
        "icon": "fas fa-music",
        "features": [
            {"icon": "fas fa-bolt", "title": "Instant Extraction", "desc": "Get your MP3 in seconds."},
            {"icon": "fas fa-shield-alt", "title": "Private & Secure", "desc": "Files are processed locally or securely."},
            {"icon": "fas fa-check-circle", "title": "High Quality", "desc": "Preserves original audio quality."}
        ]
    },
    "youtube-summary": {
        "title": "YouTube AI Summary - Convertly",
        "h1": 'YouTube <span class="gradient-text">Video Summary</span>',
        "subtitle": 'Get concise AI summaries of any YouTube video instantly.',
        "description": "Get a concise AI summary of any YouTube video instantly. Save time watching long videos.",
        "icon": "fab fa-youtube",
        "features": [
            {"icon": "fas fa-brain", "title": "AI Powered", "desc": "Advanced AI analyzes video content."},
            {"icon": "fas fa-clock", "title": "Save Time", "desc": "Get key insights without watching hours of video."},
            {"icon": "fas fa-list-ul", "title": "Key Points", "desc": "Bullet point summaries for easy reading."}
        ]
    },
    "audio-translator": {
        "title": "Free Audio Translator - Convertly",
        "h1": 'Translate <span class="gradient-text">Audio Files</span>',
        "subtitle": 'Transcribe and translate audio in over 50 languages.',
        "description": "Upload audio to get a transcription and translation in over 50 languages.",
        "icon": "fas fa-language",
        "features": [
            {"icon": "fas fa-globe", "title": "50+ Languages", "desc": "Support for all major world languages."},
            {"icon": "fas fa-file-alt", "title": "Text Output", "desc": "Get both original and translated text."},
            {"icon": "fas fa-robot", "title": "High Accuracy", "desc": "State-of-the-art speech recognition."}
        ]
    },
    "image-resizer": {
        "title": "Auto Image Resizer - Convertly",
        "h1": 'Smart <span class="gradient-text">Image Resizer</span>',
        "subtitle": 'Auto-crop images for Instagram, TikTok, and YouTube.',
        "description": "Generate social media crops (1:1, 16:9, 9:16) from a single image automatically.",
        "icon": "fas fa-crop-alt",
        "features": [
            {"icon": "fas fa-share-alt", "title": "Social Ready", "desc": "Perfect sizes for Insta, TikTok, & YouTube."},
            {"icon": "fas fa-magic", "title": "Smart Crop", "desc": "AI keeps the subject in the center."},
            {"icon": "fas fa-layer-group", "title": "Batch Gen", "desc": "Get all formats in a single ZIP."}
        ]
    },
    "privacy-redactor": {
        "title": "Document Redactor - Convertly",
        "h1": 'Privacy <span class="gradient-text">Redactor</span>',
        "subtitle": 'Blur sensitive info like emails and phones automatically.',
        "description": "Automatically redact sensitive information like emails, phone numbers, and names from text.",
        "icon": "fas fa-user-secret",
        "features": [
            {"icon": "fas fa-eye-slash", "title": "Auto Redact", "desc": "Detects emails, phones, and names."},
            {"icon": "fas fa-sliders-h", "title": "Adjustable", "desc": "Choose redaction intensity levels."},
            {"icon": "fas fa-lock", "title": "100% Private", "desc": "Processing happens in your browser."}
        ]
    },
    "site-cloner": {
        "title": "Website Cloner - Convertly",
        "h1": 'HTML <span class="gradient-text">Site Cloner</span>',
        "subtitle": 'Clone a website\'s structure, HTML, and CSS.',
        "description": "Clone a website's structure, HTML, and CSS into a clean and downloadable ZIP package.",
        "icon": "fas fa-clone",
        "features": [
            {"icon": "fas fa-code", "title": "Clean Code", "desc": "Get readable HTML and CSS."},
            {"icon": "fas fa-download", "title": "ZIP Download", "desc": "Full package ready for development."},
            {"icon": "fas fa-laptop-code", "title": "Dev Friendly", "desc": "Perfect for studying site structures."}
        ]
    },
    "code-commenter": {
        "title": "AI Code Commenter - Convertly",
        "h1": 'AI <span class="gradient-text">Code Docs</span>',
        "subtitle": 'Auto-generate JSDoc and comments for your code.',
        "description": "Auto-generate JSDoc and Docstring documentation and optimize your code formatting.",
        "icon": "fas fa-code",
        "features": [
            {"icon": "fas fa-comment-dots", "title": "Auto Docs", "desc": "Generate JSDoc and Docstrings instantly."},
            {"icon": "fas fa-align-left", "title": "Prettier", "desc": "Built-in code formatting."},
            {"icon": "fas fa-project-diagram", "title": "Multi-Lang", "desc": "Supports Python and JavaScript."}
        ]
    },
    "terminal-helper": {
        "title": "AI Terminal Helper - Convertly",
        "h1": 'Natural <span class="gradient-text">Language Terminal</span>',
        "subtitle": 'Translate natural language into safe shell commands.',
        "description": "Translate natural language into safe shell commands with risk analysis.",
        "icon": "fas fa-terminal",
        "features": [
            {"icon": "fas fa-shield-alt", "title": "Safety Checks", "desc": "AI analyzes command risk levels."},
            {"icon": "fas fa-language", "title": "Natural Polish", "desc": "Just type what you want to do."},
            {"icon": "fab fa-windows", "title": "Cross Platform", "desc": "Supports PowerShell and Bash."}
        ]
    },
    "youtube-thumbnail": {
        "title": "Free YouTube Thumbnail Background Remover - Viral Thumbnails",
        "h1": 'Viral <span class="gradient-text">Thumbnails</span>',
        "subtitle": 'Separate your subject instantly. <span class="badge-free">100% Free</span>',
        "description": "Create viral YouTube thumbnails instantly. Remove backgrounds from your selfies and reaction shots. 100% Free.",
        "icon": "fab fa-youtube",
        "features": [
            {"icon": "fas fa-fire", "title": "High CTR", "desc": "Clean cutouts increase click-through rates."},
            {"icon": "fas fa-magic", "title": "AI Precision", "desc": "Perfect hair and edge detection."},
            {"icon": "fas fa-bolt", "title": "Instant", "desc": "Get your cutout in seconds."}
        ]
    }
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

def generate_pages():
    # Read Template (Main Index)
    template_path = os.path.join(FRONTEND_DIR, 'index.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_html = f.read()

    for tool_key, config in TOOLS.items():
        print(f"Generating page for: {tool_key}")
        
        # 1. Prepare Template Soup
        soup = BeautifulSoup(template_html, 'html.parser')
        
        # 2. Adjust Relative Paths (Up 2 levels: tools/<tool>/index.html -> ../../)
        for tag in soup.find_all(['link', 'a', 'img', 'script']):
            if tag.has_attr('href'):
                href = tag['href']
                if not href.startswith('http') and not href.startswith('#') and not href.startswith('mailto:'):
                    tag['href'] = '../../' + href
            if tag.has_attr('src'):
                src = tag['src']
                if not src.startswith('http') and not src.startswith('data:'):
                    tag['src'] = '../../' + src
        
        # 3. Customize Head
        soup.title.string = config['title']
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            meta_desc['content'] = config['description']
        
        # Open Graph & Twitter adjustments could go here...

        # 4. Extract Tool UI from existing tool page
        tool_path = os.path.join(FRONTEND_DIR, 'tools', tool_key, 'index.html')
        if not os.path.exists(tool_path):
            print(f"Skipping {tool_key}: Path not found {tool_path}")
            continue

        with open(tool_path, 'r', encoding='utf-8') as f:
            tool_soup = BeautifulSoup(f.read(), 'html.parser')

        # Find the core content (usually .tool-content or .upload-container depends on tool)
        # We look for .tool-content first, then specific containers
        tool_content = tool_soup.find(class_='tool-content')
        if not tool_content:
            tool_content = tool_soup.find(class_='upload-container')
        
        if not tool_content:
            print(f"Warning: Could not find content for {tool_key}")
            continue

        # Extract Scripts (Inline and External specific to tool)
        tool_scripts = tool_soup.find_all('script')
        scripts_to_inject = []
        for script in tool_scripts:
            # Skip common scripts if they are already in template (like script.js if we kept it, but we wont)
            # Actually, we should keep tool specific external scripts (like ImageResizer.js)
            # And all inline logic
            scripts_to_inject.append(script)
            
        unique_scripts = []

        # 5. Inject into Template Hero
        # Find hero section to replace
        hero_div = soup.find(class_='hero')
        if hero_div:
            # Update H1 and Subtitle
            h1 = hero_div.find('h1')
            if h1:
                h1.decode_contents() # clear
                h1.innerHTML = config['h1'] # BeautifulSoup doesn't have innerHTML, use append
                h1.clear()
                # We need to render the HTML string for H1 since it contains spans
                h1_soup = BeautifulSoup(config['h1'], 'html.parser')
                h1.append(h1_soup)
            
            subtitle = hero_div.find(class_='subtitle')
            if subtitle:
                subtitle.string = config['subtitle']

            # Remove existing upload-container / editor-container from template
            for cls in ['upload-container', 'processing-content', 'editor-container', 'batch-container']:
                existing = hero_div.find(class_=cls)
                if existing:
                    existing.decompose()
        
        # Remove SEO Content Block (it's outside hero now, so find in soup)
        seo_content = soup.find(class_='seo-content')
        if seo_content:
            seo_content.decompose()
            
            # Append Tool UI
            hero_div.append(tool_content)

        # 6. Update Features
        features_div = soup.find(class_='features')
        if features_div:
            features_div.clear() # Remove old features
            for feature in config['features']:
                feat_item = soup.new_tag('div', attrs={'class': 'feature-item'})
                
                icon_div = soup.new_tag('div', attrs={'class': 'feature-icon'})
                icon_i = soup.new_tag('i', attrs={'class': feature['icon']})
                icon_div.append(icon_i)
                
                h3 = soup.new_tag('h3')
                h3.string = feature['title']
                
                p = soup.new_tag('p')
                p.string = feature['desc']
                
                feat_item.append(icon_div)
                feat_item.append(h3)
                feat_item.append(p)
                features_div.append(feat_item)

        # 7. Inject Scripts at Body End
        
        # Inject Desktop Detection Script
        desktop_script = soup.new_tag('script')
        desktop_script.string = """
        (function() {
            const urlParams = new URLSearchParams(window.location.search);
            if (window.pywebview !== undefined || urlParams.get('app') === 'desktop') {
                sessionStorage.setItem('isDesktop', 'true');
            }
        })();
        """
        soup.body.append(desktop_script)

        # Remove the default script.js from template if it's there (bg remover logic)
        # Template has <script src="../../script.js?v=2.0"></script> after adjustment
        body = soup.body
        scripts_to_remove = body.find_all('script', src=lambda s: s and 'script.js' in s)
        for s in scripts_to_remove:
            s.decompose()

            # 7.1 Garbage Collection (Fix broken patches from previous runs)
            if script.string:
                # Remove orphaned code blocks starting with e.preventDefault() at root level
                import re
                # This regex looks for the specific garbage pattern created by the previous bad patch
                # Matches: e.preventDefault(); ... return; }
                script.string = re.sub(r'e\.preventDefault\(\);[\s\S]*?return;\s*}', '', script.string)
                
                # Deduplicate checkEnvironment and other common function re-declarations
                if 'function checkEnvironment()' in script.string:
                     # If we already have a script with exactly this content in scripts_to_inject, skip
                     pass 

            # 7.2 Safe Patching of handleSmartDownload
            if script.string and 'function handleSmartDownload' in script.string:
                # 1. Rename existing function to _unused to wrap old body safely
                script.string = script.string.replace(
                    'function handleSmartDownload(e, url, filename) {', 
                    'function _unused_old_handler(e, url, filename) {'
                )
                
                # 2. Append the NEW clean function at the end of the script
                # We append it to the end to ensure it overrides/exists globally
                script.string += """
                
                // Fixed Direct Download Handler
                function handleSmartDownload(e, url, filename) {
                    e.preventDefault();
                    console.log('Smart Link Removed -> Direct Download');
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = filename;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }
                """

            # 7.3 Deduplication Strategy
            # Use a hash of the script content to check for uniqueness
            import hashlib
            content_hash = hashlib.md5(script.encode_contents().strip()).hexdigest() if hasattr(script, 'encode_contents') else hashlib.md5(str(script).encode('utf-8').strip()).hexdigest()
            
            if content_hash not in [s['hash'] for s in unique_scripts]:
                unique_scripts.append({'hash': content_hash, 'tag': script})
            
        # Append Unique Scripts Only
        for s in unique_scripts:
            body.append(s['tag'])

        # 8. Write Output
        with open(tool_path, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))

if __name__ == "__main__":
    generate_pages()
