import os
import shutil
import datetime

# Configuration
BASE_URL = "https://convertly.up.railway.app"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(SCRIPT_DIR, "../frontend")
SITEMAP_PATH = os.path.join(FRONTEND_DIR, "sitemap.xml")
INDEX_PATH = os.path.join(FRONTEND_DIR, "index.html")

# Data for Use-Case Pages
USE_CASES = {
    "cars": {
        "title": "Free Car Background Remover - Auto & Vehicle Photography",
        "description": "Remove backgrounds from car photos instantly. Perfect for dealerships, marketplaces, and auto photographers. 100% Free.",
        "keywords": "remove car background, car photography editing, dealership photo tool, vehicle background remover, auto image editor",
        "h1": "Remove <span class=\"gradient-text\">Car Backgrounds</span>",
        "subtitle": "Professional car photography in seconds. <span class=\"badge-free\">Free for Dealerships</span>",
        "icon": "fa-car",
        "feat1_title": "Clean Edges",
        "feat1_desc": "Perfectly handles windows, shadows, and reflections.",
        "feat2_title": "Dealer Ready",
        "feat2_desc": "Consistent white backgrounds for inventory listings.",
    },
    "jewelry": {
        "title": "Jewelry Background Remover - AI for Rings & Necklaces",
        "description": "Make jewelry photos pop with white backgrounds. Remove background from rings, necklaces, and earrings instantly.",
        "keywords": "jewelry background remover, remove background from ring, necklace photo editor, white background for jewelry, ecommerce photography",
        "h1": "Enhance <span class=\"gradient-text\">Jewelry Photos</span>",
        "subtitle": "Sparkling results for your online store. <span class=\"badge-free\">100% Free</span>",
        "icon": "fa-gem",
        "feat1_title": "Macro Precision",
        "feat1_desc": "Captures intricate details and fine chains.",
        "feat2_title": "Shine Boost",
        "feat2_desc": "Maintains the natural sparkle of gemstones.",
    },
    "shoes": {
        "title": "Shoe Background Remover - Sneaker Photography Tool",
        "description": "Remove backgrounds from shoes and sneakers. Create professional product shots for StockX, Goat, and Shopify.",
        "keywords": "remove sneaker background, shoe photo editor, product photography, sneakerhead tools, white background for shoes",
        "h1": "Edit <span class=\"gradient-text\">Shoe Photos</span>",
        "subtitle": "Level up your sneaker game. <span class=\"badge-free\">Instant Download</span>",
        "icon": "fa-shoe-prints",
        "feat1_title": "Sole Detection",
        "feat1_desc": "Perfectly outlines soles and laces.",
        "feat2_title": "Marketplace Ready",
        "feat2_desc": "Optimized for StockX and eBay standards.",
    },
    "furniture": {
        "title": "Furniture Background Remover - Home Decor Editing",
        "description": "Remove background from furniture photos. Sofas, chairs, tables - clean cutouts for interior design.",
        "keywords": "furniture background remover, remove background from sofa, interior design tool, home staging, product photos",
        "h1": "Clean <span class=\"gradient-text\">Furniture Shots</span>",
        "subtitle": "Showcase your designs without distractions. <span class=\"badge-free\">Free Tool</span>",
        "icon": "fa-couch",
        "feat1_title": "Large Objects",
        "feat1_desc": "Handles large items and complex shadows.",
        "feat2_title": "Texture Safe",
        "feat2_desc": "Preserves fabric textures and wood grains.",
    },
    "animals": {
        "title": "Pet Background Remover - Animal Photography",
        "description": "Remove background from dog and cat photos. AI handles fur and whiskers perfectly.",
        "keywords": "remove background from dog, cat photo editor, pet photography, animal background remover, fluffy",
        "h1": "Cute <span class=\"gradient-text\">Pet Portraits</span>",
        "subtitle": "Focus on your furry friends. <span class=\"badge-free\">Purr-fect Results</span>",
        "icon": "fa-paw",
        "feat1_title": "Fur Technology",
        "feat1_desc": "Smart AI detects individual strands of fur.",
        "feat2_title": "Whiskers Safe",
        "feat2_desc": "Does not blur or cut off sensitive details.",
    },
    "people": {
        "title": "Portrait Background Remover - Headshots & Selfies",
        "description": "Remove background from portraits and selfies. Create professional headshots or fun stickers.",
        "keywords": "remove background from person, selfie background remover, headshot creator, human background removal, face cutout",
        "h1": "Professional <span class=\"gradient-text\">Portraits</span>",
        "subtitle": "Upgrade your profile pic instantly. <span class=\"badge-free\">Studio Quality</span>",
        "icon": "fa-user",
        "feat1_title": "Hair Fine-Tuning",
        "feat1_desc": "Handles loose hair and complex hairstyles.",
        "feat2_title": "Face Focus",
        "feat2_desc": "Keeps facial features sharp and natural.",
    },
    "real-estate": {
        "title": "Real Estate Background Remover - House & Property",
        "description": "Clean up property photos. Remove sky or cluttered backgrounds from real estate listings.",
        "keywords": "real estate photo editing, remove sky, property background, house photo tool, realtor tools",
        "h1": "Stunning <span class=\"gradient-text\">Property Photos</span>",
        "subtitle": "Sell homes faster with clean images. <span class=\"badge-free\">Realtor Friendly</span>",
        "icon": "fa-home",
        "feat1_title": "Sky Ready",
        "feat1_desc": "Easily prepare photos for sky replacement.",
        "feat2_title": "Angle Correction",
        "feat2_desc": "Works well with wide-angle lens shots.",
    },
    "graphics": {
        "title": "Graphic Background Remover - Icons & Anime",
        "description": "Remove background from anime, cartoons, and digital art. Create transparent sprites and assets.",
        "keywords": "remove anime background, cartoon background remover, sprite maker, vtuber tools, digital art",
        "h1": "Transparent <span class=\"gradient-text\">Graphics</span>",
        "subtitle": "For content creators and artists. <span class=\"badge-free\">Asset Ready</span>",
        "icon": "fa-paint-brush",
        "feat1_title": "Hard Edges",
        "feat1_desc": "Crisp cuts for digital lines and art.",
        "feat2_title": "Alpha Channel",
        "feat2_desc": "Perfect transparency for game assets.",
    },
    "signatures": {
        "title": "Signature Background Remover - Digital Sig Maker",
        "description": "Digitize your signature. Remove background from handwritten signatures for documents.",
        "keywords": "remove background from signature, digital signature maker, transparent signature, sign pdf, document tools",
        "h1": "Digital <span class=\"gradient-text\">Signatures</span>",
        "subtitle": "Sign documents professionally. <span class=\"badge-free\">Secure & Fast</span>",
        "icon": "fa-file-signature",
        "feat1_title": "Ink Extraction",
        "feat1_desc": "Isolates ink from paper texture.",
        "feat2_title": "High Contrast",
        "feat2_desc": "Ensures your signature is bold and visible.",
    }
}

# Data for Languages
LANGUAGES = {
    "fr": {
        "name": "Français",
        "title": "Convertly - Supprimeur d'arrière-plan IA Gratuit",
        "desc": "Supprimez les arrière-plans automatiquement en 5 secondes. Gratuit et de haute qualité.",
        "h1": "Supprimer l'<span class=\"gradient-text\">Arrière-plan</span>",
        "subtitle": "100% Automatique et <span class=\"badge-free\">Gratuit</span>",
        "upload_btn": "Télécharger une Image",
        "drop_text": "ou déposez votre photo ici",
        "processing": "Suppression de l'arrière-plan...",
        "download_hd": "Télécharger HD",
        "download_free": "Gratuit avec Filigrane",
        "features": [
            {"title": "Détection Auto", "desc": "Notre IA détecte les sujets en millisecondes."},
            {"title": "Haute Qualité", "desc": "Préservez la qualité originale de vos photos."},
            {"title": "Rapide & Gratuit", "desc": "Traitement instantané sans inscription."}
        ],
        "pricing": {
            "title": "Choisissez votre plan",
            "free": "Gratuit",
            "pro": "Pro",
            "best_value": "MEILLEURE VALEUR",
             "per_mo": "/mois"
        },
        "footer": {
             "terms": "Conditions",
             "contact": "Contact",
             "refund": "Remboursement",
             "faq": "FAQ"
        }
    },
    "it": {
        "name": "Italiano",
        "title": "Convertly - Rimozione Sfondo AI Gratis",
        "desc": "Rimuovi gli sfondi automaticamente in 5 secondi. Gratis e alta qualità.",
        "h1": "Rimuovi <span class=\"gradient-text\">Sfondo</span>",
        "subtitle": "100% Automatico e <span class=\"badge-free\">Gratis</span>",
        "upload_btn": "Carica Immagine",
        "drop_text": "o trascina la tua foto qui",
        "processing": "Rimozione sfondo...",
        "download_hd": "Scarica HD",
        "download_free": "Gratis con Filigrana",
        "features": [
            {"title": "Rilevamento Auto", "desc": "La nostra AI rileva i soggetti in millisecondi."},
            {"title": "Alta Qualità", "desc": "Preserva la qualità originale delle tue foto."},
            {"title": "Veloce & Gratis", "desc": "Elaborazione istantanea senza registrazione."}
        ],
        "pricing": {
            "title": "Scegli il tuo piano",
            "free": "Gratis",
            "pro": "Pro",
            "best_value": "MIGLIOR VALORE",
             "per_mo": "/mese"
        },
        "footer": {
             "terms": "Termini",
             "contact": "Contatti",
             "refund": "Rimborsi",
             "faq": "FAQ"
        }
    },
    "es": {
        "name": "Español",
        "title": "Convertly - Quitafondos IA Gratis",
        "desc": "Elimina fondos automáticamente en 5 segundos. Gratis y alta calidad.",
        "h1": "Eliminar <span class=\"gradient-text\">Fondo</span>",
        "subtitle": "100% Automático y <span class=\"badge-free\">Gratis</span>",
        "upload_btn": "Subir Imagen",
        "drop_text": "o suelta tu foto aquí",
        "processing": "Eliminando fondo...",
        "download_hd": "Descargar HD",
        "download_free": "Gratis con Marca de Agua",
        "features": [
            {"title": "Detección Auto", "desc": "Nuestra IA detecta sujetos en milisegundos."},
            {"title": "Alta Calidad", "desc": "Preserva la calidad original de tus fotos."},
            {"title": "Rápido y Gratis", "desc": "Procesamiento instantáneo sin registro."}
        ],
        "pricing": {
            "title": "Elige tu plan",
            "free": "Gratis",
            "pro": "Pro",
            "best_value": "MEJOR VALOR",
             "per_mo": "/mes"
        },
        "footer": {
             "terms": "Términos",
             "contact": "Contacto",
             "refund": "Reembolso",
             "faq": "FAQ"
        }
    },
    "pt": {
        "name": "Português",
        "title": "Convertly - Removedor de Fundo IA Grátis",
        "desc": "Remova fundos automaticamente em 5 segundos. Grátis e alta qualidade.",
        "h1": "Remover <span class=\"gradient-text\">Fundo</span>",
        "subtitle": "100% Automático e <span class=\"badge-free\">Grátis</span>",
        "upload_btn": "Carregar Imagem",
        "drop_text": "ou solte sua foto aqui",
        "processing": "Removendo fundo...",
        "download_hd": "Baixar HD",
        "download_free": "Grátis com Marca D'água",
        "features": [
            {"title": "Detecção Auto", "desc": "Nossa IA detecta assuntos em milissegundos."},
            {"title": "Alta Qualidade", "desc": "Preserve a qualidade original de suas fotos."},
            {"title": "Rápido e Grátis", "desc": "Processamento instantâneo sem registro."}
        ],
        "pricing": {
            "title": "Escolha seu plano",
            "free": "Grátis",
            "pro": "Pro",
            "best_value": "MELHOR VALOR",
             "per_mo": "/mês"
        },
        "footer": {
             "terms": "Termos",
             "contact": "Contato",
             "refund": "Reembolso",
             "faq": "FAQ"
        }
    },
    "nl": {
        "name": "Nederlands",
        "title": "Convertly - Gratis AI Achtergrond Verwijderaar",
        "desc": "Verwijder achtergronden automatisch in 5 seconden. Gratis en hoge kwaliteit.",
        "h1": "Verwijder <span class=\"gradient-text\">Achtergrond</span>",
        "subtitle": "100% Automatisch en <span class=\"badge-free\">Gratis</span>",
        "upload_btn": "Upload Afbeelding",
        "drop_text": "of sleep je foto hier",
        "processing": "Achtergrond verwijderen...",
        "download_hd": "Download HD",
        "download_free": "Gratis met Watermerk",
        "features": [
            {"title": "Auto Detectie", "desc": "Onze AI detecteert onderwerpen in milliseconden."},
            {"title": "Hoge Kwaliteit", "desc": "Behoud de originele kwaliteit van uw foto's."},
            {"title": "Snel & Gratis", "desc": "Directe verwerking zonder registratie."}
        ],
        "pricing": {
            "title": "Kies je plan",
            "free": "Gratis",
            "pro": "Pro",
            "best_value": "BESTE WAARDE",
             "per_mo": "/maand"
        },
        "footer": {
             "terms": "Voorwaarden",
             "contact": "Contact",
             "refund": "Terugbetaling",
             "faq": "FAQ"
        }
    },
    "ru": {
        "name": "Русский",
        "title": "Convertly - Бесплатное удаление фона",
        "desc": "Автоматическое удаление фона за 5 секунд. Бесплатно и качественно.",
        "h1": "Удалить <span class=\"gradient-text\">Фон</span>",
        "subtitle": "100% Автоматически и <span class=\"badge-free\">Бесплатно</span>",
        "upload_btn": "Загрузить Фото",
        "drop_text": "или перетащите фото сюда",
        "processing": "Удаление фона...",
        "download_hd": "Скачать HD",
        "download_free": "Бесплатно с знаком",
        "features": [
            {"title": "Автообнаружение", "desc": "Наш ИИ обнаруживает объекты за миллисекунды."},
            {"title": "Высокое Качество", "desc": "Сохраняйте оригинальное качество фотографий."},
            {"title": "Быстро и Бесплатно", "desc": "Мгновенная обработка без регистрации."}
        ],
        "footer": {
             "terms": "Условия",
             "contact": "Контакты",
             "refund": "Возврат",
             "faq": "FAQ"
        }
    },
    "de": {
        "name": "Deutsch",
        "title": "Convertly - Kostenloser KI Hintergrund-Entferner",
        "desc": "Entfernen Sie Hintergründe automatisch in 5 Sekunden. Kostenlos und in hoher Qualität.",
        "h1": "<span class=\"gradient-text\">Hintergrund</span> entfernen",
        "subtitle": "100% Automatisch und <span class=\"badge-free\">Kostenlos</span>",
        "upload_btn": "Bild hochladen",
        "drop_text": "oder Bild hier ablegen",
        "processing": "Hintergrund wird entfernt...",
        "download_hd": "Werbung ansehen für HD (Kostenlos)",
        "download_free": "Standard Herunterladen (Kostenlos)",
        "features": [
            {"title": "Auto Erkennung", "desc": "Unsere KI erkennt Motive in Millisekunden."},
            {"title": "Hohe Qualität", "desc": "Erhalten Sie die Originalqualität Ihrer Fotos."},
            {"title": "Schnell & Gratis", "desc": "Sofortige Bearbeitung ohne Anmeldung."}
        ],
        "footer": {
             "terms": "AGB",
             "contact": "Kontakt",
             "refund": "Rückerstattung",
             "faq": "FAQ"
        }
    }
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang_code}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="Convertly">
    <meta name="robots" content="index, follow">
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="{url}">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{description}">
    <link rel="canonical" href="{url}">
    {hreflang_tags}
    <link rel="stylesheet" href="{css_path}style.css?v=1.2">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "Convertly",
      "applicationCategory": "MultimediaApplication",
      "operatingSystem": "Web",
      "offers": {{
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
      }},
      "description": "{description}",
      "aggregateRating": {{
        "@type": "AggregateRating",
        "ratingValue": "4.8",
        "ratingCount": "1250"
      }}
    }}
    </script>
    <script src="https://www.paypal.com/sdk/js?client-id=test&currency=USD"></script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8446489406681308" crossorigin="anonymous"></script>
</head>
<body>
    <div class="bg-blobs">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
    </div>
    <nav>
        <div class="logo">
            <a href="{home_link}" style="text-decoration: none; color: inherit; display: flex; align-items: center; gap: 10px;">
                <div class="logo-icon"><i class="fas fa-layer-group"></i></div>
                <span>CONVERTLY</span>
            </a>
        </div>
        <div class="nav-links">
            <a href="#" id="view-uploads" class="nav-btn">Uploads</a>
        </div>
    </nav>
    <main>
        <div class="hero">
            <h1>{h1}</h1>
            <p class="subtitle">{subtitle}</p>
            <div class="upload-container" id="upload-container">
                <div class="upload-content" id="upload-content">
                    <div class="upload-icon"><i class="{main_icon}"></i></div>
                    <button class="upload-btn" onclick="document.getElementById('file-input').click()">{upload_btn}</button>
                    <p class="drop-text">{drop_text}</p>
                    <input type="file" id="file-input" accept="image/*" hidden>
                </div>
                <div class="processing-content" id="processing-content" style="display: none;">
                    <div class="spinner"></div>
                    <p>{processing_text}</p>
                </div>
                <div class="result-content" id="result-content" style="display: none;">
                    <img id="result-image" src="" alt="Processed Image">
                    <div class="result-actions">
                        <button class="download-btn" id="download-hd-btn">{download_hd} <i class="fas fa-play-circle" style="font-size: 0.8em; margin-left: 5px;"></i></button>
                        <button class="download-watermark-btn" id="download-watermark-btn">{download_free}</button>
                        <button class="reset-btn" id="reset-btn">Upload Another</button>
                    </div>
                </div>
            </div>
            {comparison_visual}
        </div>
        <div id="ad-modal" class="ad-modal" style="display: none;">
             <div class="ad-content">
                <div class="ad-header">
                    <h3>Watch Ad</h3>
                    <button class="close-ad" id="close-ad">&times;</button>
                </div>
                <div class="ad-body">
                    <div class="ad-placeholder">
                        <div class="ad-timer" id="ad-timer">5</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="features">
            <div class="feature-item">
                <div class="feature-icon"><i class="fas fa-shield-alt"></i></div>
                <h3>{feat1_title}</h3>
                <p>{feat1_desc}</p>
            </div>
            <div class="feature-item">
                <div class="feature-icon"><i class="fas fa-bolt"></i></div>
                <h3>{feat2_title}</h3>
                <p>{feat2_desc}</p>
            </div>
            <div class="feature-item">
                <div class="feature-icon"><i class="far fa-clock"></i></div>
                <h3>{feat3_title}</h3>
                <p>{feat3_desc}</p>
            </div>
        </div>
    </main>
    <footer>
        <button id="footer-toggle-btn" class="footer-toggle-btn" onclick="toggleFooter()">
            <span>{footer_expander_text}</span>
            <i class="fas fa-chevron-down" id="footer-toggle-icon"></i>
        </button>
        
        <div id="footer-directory" class="footer-directory" style="display: none;">
            <div class="footer-grid">
                <div class="footer-column">
                    <h4>{footer_col1_title}</h4>
                    <a href="{home_link}#">{footer_uploads}</a>
                    <a href="{logo_remover_link}">{footer_logo_remover}</a>
                </div>
                <div class="footer-column">
                    <h4>{footer_col2_title}</h4>
                    {footer_use_cases}
                </div>
                <div class="footer-column">
                    <h4>{footer_col3_title}</h4>
                    {footer_languages}
                </div>
                <div class="footer-column">
                    <h4>{footer_col4_title}</h4>
                    <a href="#">{footer_terms}</a>
                    <a href="#">{footer_contact}</a>
                    <a href="#">{footer_refund}</a>
                    <a href="#">{footer_faq}</a>
                </div>
            </div>
        </div>

        <div class="social-links">
            <a href="#"><i class="fab fa-twitter"></i></a>
            <a href="#"><i class="fab fa-instagram"></i></a>
        </div>
        <p class="copyright">© 2024 CONVERTLY. Created with Love.</p>
    </footer>

    <script>
        function toggleFooter() {{
            const dir = document.getElementById('footer-directory');
            const icon = document.getElementById('footer-toggle-icon');
            if (dir.style.display === 'none') {{
                dir.style.display = 'block';
                icon.style.transform = 'rotate(180deg)';
            }} else {{
                dir.style.display = 'none';
                icon.style.transform = 'rotate(0deg)';
            }}
        }}
    </script>
    <script src="{js_path}script.js"></script>
</body>
</html>
"""

def generate_use_cases():
    print("Generating use-case pages...")
    
    # Hreflang
    hreflangs = f'<link rel="alternate" hreflang="en" href="{BASE_URL}/" />\n'
    for lang in LANGUAGES.keys():
        hreflangs += f'    <link rel="alternate" hreflang="{lang}" href="{BASE_URL}/{lang}/" />\n'

    # Prepare footer links (English)
    use_case_links_str = '\n'.join([f'<a href="{k}.html">{v["title"].split("-")[0].strip()}</a>' for k,v in USE_CASES.items()])
    lang_links_str = '\n'.join([f'<a href="{k}/index.html">{v["name"]}</a>' for k,v in LANGUAGES.items()])

    for slug, data in USE_CASES.items():
        filename = f"{slug}.html"
        filepath = os.path.join(FRONTEND_DIR, filename)
        
        # Default Features
        feat1_t = data.get("feat1_title", "Automatic Detection")
        feat1_d = data.get("feat1_desc", "Our AI detects subjects in milliseconds.")
        feat2_t = data.get("feat2_title", "High Quality")
        feat2_d = data.get("feat2_desc", "Preserve original quality.")
        
        content = HTML_TEMPLATE.format(
            lang_code="en",
            title=data["title"],
            description=data["description"],
            keywords=data["keywords"],
            url=f"{BASE_URL}/{filename}",
            hreflang_tags="", 
            css_path="",
            home_link="index.html",
            h1=data["h1"],
            subtitle=data["subtitle"],
            main_icon=data.get("icon", "far fa-image"),
            upload_btn="Upload Image",
            drop_text="or drop your image here",
            processing_text="Removing background...",
            comparison_visual="", # No visual on use-case pages to avoid context clash (e.g. sneaker on car page)
            download_hd="Watch Ad to Download HD (Free)",
            download_free="Download Standard (Free)",
            feat1_title=feat1_t,
            feat1_desc=feat1_d,
            feat2_title=feat2_t,
            feat2_desc=feat2_d,
            feat3_title="Fast & Free",
            feat3_desc="Instant processing without registration.",
            js_path="",
            # New Footer Variables
            footer_expander_text="Explore Convertly (Use Cases & Languages)",
            footer_col1_title="Product",
            footer_uploads="Uploads",
            footer_pricing="Pricing",
            footer_logo_remover="Logo Remover",
            logo_remover_link="logos.html",
            footer_col2_title="Use Cases",
            footer_use_cases=use_case_links_str,
            footer_col3_title="Languages",
            footer_languages=lang_links_str,
            footer_col4_title="Company",
            footer_terms="Terms of Service",
            footer_contact="Contact",
            footer_refund="Refund Policy",
            footer_faq="FAQ"
        )
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created {filename}")

def generate_root_index():
    print("Generating root index.html...")
    
    # Hreflang
    hreflangs = f'<link rel="alternate" hreflang="en" href="{BASE_URL}/" />\n'
    for lang in LANGUAGES.keys():
        hreflangs += f'    <link rel="alternate" hreflang="{lang}" href="{BASE_URL}/{lang}/" />\n'

    # Footer Links
    use_case_links_str = '\n'.join([f'<a href="{k}.html">{v["title"].split("-")[0].strip()}</a>' for k,v in USE_CASES.items()])
    lang_links_str = '\n'.join([f'<a href="{k}/index.html">{v["name"]}</a>' for k,v in LANGUAGES.items()])

    content = HTML_TEMPLATE.format(
        lang_code="en",
        title="Free Background Remover - Convertly",
        description="Remove image backgrounds automatically in 5 seconds. High quality, free, and instant results.",
        keywords="background remover, remove background, ai background removal, transparent background, free background remover, convertly",
        url=f"{BASE_URL}/",
        hreflang_tags=hreflangs,
        css_path="",
        home_link="index.html",
        h1="Remove <span class=\"gradient-text\">Background</span>",
        subtitle="100% Automatic and <span class=\"badge-free\">Free</span>",
        main_icon="far fa-image",
        upload_btn="Upload Image",
        drop_text="or drop your image here",
        processing_text="Removing background...",
        # Before/After Visual Removed
        comparison_visual="",
        download_hd="Watch Ad to Download HD (Free)",
        download_free="Download Standard (Free)",
        feat1_title="Auto Detection",
        feat1_desc="Our AI detects subjects in milliseconds.",
        feat2_title="High Quality",
        feat2_desc="Preserve original quality.",
        feat3_title="Fast & Free",
        feat3_desc="Instant processing without registration.",
        js_path="",
        # Footer
        footer_expander_text="Explore Convertly",
        footer_col1_title="Product",
        footer_uploads="Uploads",
        footer_logo_remover="Logo Remover",
        logo_remover_link="logos.html",
        footer_col2_title="Use Cases",
        footer_use_cases=use_case_links_str,
        footer_col3_title="Languages",
        footer_languages=lang_links_str,
        footer_col4_title="Company",
        footer_terms="Terms",
        footer_contact="Contact",
        footer_refund="Refunds",
        footer_faq="FAQ"
    )
    
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("Created index.html")


def generate_languages():
    print("Generating language pages...")
    
    hreflangs = f'<link rel="alternate" hreflang="en" href="{BASE_URL}/" />\n'
    for lang in LANGUAGES.keys():
        hreflangs += f'    <link rel="alternate" hreflang="{lang}" href="{BASE_URL}/{lang}/" />\n'

    # Prepare footer links (Localized paths need ../)
    use_case_links_str = '\n'.join([f'<a href="../{k}.html">{v["title"].split("-")[0].strip()}</a>' for k,v in USE_CASES.items()])
    
    for lang_code, data in LANGUAGES.items():
        lang_dir = os.path.join(FRONTEND_DIR, lang_code)
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
        
        filepath = os.path.join(lang_dir, "index.html")
        
        # Build language links for this specific language page
        # Include English + other languages
        lang_links_list = [f'<a href="../index.html">English</a>']
        for l_code, l_data in LANGUAGES.items():
            if l_code != lang_code:
                lang_links_list.append(f'<a href="../{l_code}/index.html">{l_data["name"]}</a>')
        lang_links_str = '\n'.join(lang_links_list)

        content = HTML_TEMPLATE.format(
            lang_code=lang_code,
            title=data["title"],
            description=data["desc"],
            keywords=f"background remover {lang_code}, remove background",
            url=f"{BASE_URL}/{lang_code}/",
            hreflang_tags=hreflangs,
            css_path="../",
            home_link="../index.html",
            h1=data["h1"],
            subtitle=data["subtitle"],
            main_icon="far fa-image",
            upload_btn=data["upload_btn"],
            drop_text=data["drop_text"],
            processing_text=data["processing"],
            comparison_visual="", # No visual on translated pages for now to save space/complexity
            download_hd=data["download_hd"],
            download_free=data["download_free"],
            feat1_title=data["features"][0]["title"],
            feat1_desc=data["features"][0]["desc"],
            feat2_title=data["features"][1]["title"],
            feat2_desc=data["features"][1]["desc"],
            feat3_title=data["features"][2]["title"],
            feat3_desc=data["features"][2]["desc"],
            js_path="../",
            # New Footer Variables (Localized)
            footer_expander_text="Explore Convertly", # Simplified for now
            footer_col1_title="Product",
            footer_uploads="Uploads",
            footer_logo_remover="Logo Remover",
            logo_remover_link="../logos.html",
            footer_col2_title="Use Cases",
            footer_use_cases=use_case_links_str,
            footer_col3_title="Languages",
            footer_languages=lang_links_str,
            footer_col4_title="Company",
            footer_terms=data["footer"]["terms"],
            footer_contact=data["footer"]["contact"],
            footer_refund=data["footer"]["refund"],
            footer_faq=data["footer"]["faq"]
        )
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created {lang_code}/index.html")

def update_sitemap():
    print("Updating sitemap...")
    urls = [f"{BASE_URL}/"]
    
    # Use cases
    for slug in USE_CASES.keys():
        urls.append(f"{BASE_URL}/{slug}.html")
    
    # Languages
    for lang in LANGUAGES.keys():
        urls.append(f"{BASE_URL}/{lang}/")
        
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        sitemap_content += f"""   <url>
      <loc>{url}</loc>
      <lastmod>{datetime.date.today()}</lastmod>
      <changefreq>weekly</changefreq>
      <priority>0.8</priority>
   </url>\n"""
   
    sitemap_content += '</urlset>'
    
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print("Sitemap updated.")

if __name__ == "__main__":
    generate_root_index()
    generate_use_cases()
    generate_languages()
    update_sitemap()
