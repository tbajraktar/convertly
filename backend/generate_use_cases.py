from bs4 import BeautifulSoup
import os

# Configuration for all Use Case Pages
USE_CASES = {
    # Existing Use Cases (Regenerating to ensure consistency)
    'cars': {
        'title': 'Free Car Background Remover - Auto & Vehicle Photography',
        'description': 'Remove backgrounds from car photos instantly. Perfect for dealerships, marketplaces, and auto photographers. 100% Free.',
        'keywords': 'remove car background, car photography editing, dealership photo tool, vehicle background remover, auto image editor',
        'h1': 'Remove <span class="gradient-text">Car Backgrounds</span>',
        'subtitle': 'Professional car photography in seconds. <span class="badge-free">Free for Dealerships</span>',
        'icon': 'fa-car',
        'features': [
            {'icon': 'fas fa-shield-alt', 'title': 'Clean Edges', 'desc': 'Perfectly handles windows, shadows, and reflections.'},
            {'icon': 'fas fa-bolt', 'title': 'Dealer Ready', 'desc': 'Consistent white backgrounds for inventory listings.'},
            {'icon': 'far fa-clock', 'title': 'Fast & Free', 'desc': 'Instant processing without registration.'}
        ]
    },
    'jewelry': {
        'title': 'Free Jewelry Background Remover - Product Photography',
        'description': 'Create stunning white-background jewelry photos. Preserve sparkle, shine, and intricate details automatically.',
        'keywords': 'jewelry background remover, necklace photo editor, ring background removal, product photography tool',
        'h1': 'Enhance <span class="gradient-text">Jewelry Photos</span>',
        'subtitle': 'Studio-quality results for rings, necklaces, and earrings.',
        'icon': 'fa-gem',
        'features': [
            {'icon': 'fas fa-magic', 'title': 'Preserve Shine', 'desc': 'Keeps natural reflections and sparkle intact.'},
            {'icon': 'fas fa-search', 'title': 'Macro Detail', 'desc': 'High-resolution processing for intricate designs.'},
            {'icon': 'fas fa-shopping-bag', 'title': 'Sales Ready', 'desc': 'Perfect white backgrounds for online stores.'}
        ]
    },
    'shoes': {
        'title': 'Free Shoe Background Remover - Sneaker Photography',
        'description': 'Remove backgrounds from shoe photos instantly. perfect for sneakerheads, resellers, and e-commerce stores.',
        'keywords': 'shoe background remover, sneaker photo editor, footwear photography, white background shoes',
        'h1': 'Edit <span class="gradient-text">Shoe Photos</span>',
        'subtitle': 'Clean cutouts for sneakers, heels, and boots.',
        'icon': 'fa-shoe-prints',
        'features': [
            {'icon': 'fas fa-cut', 'title': 'Precision Cut', 'desc': 'Accurate edges around laces and soles.'},
            {'icon': 'fas fa-store', 'title': 'Marketplace Ready', 'desc': 'Optimized for StockX, GOAT, and eBay.'},
            {'icon': 'fas fa-bolt', 'title': 'Instant', 'desc': 'Process hundreds of photos in minutes.'}
        ]
    },
    'furniture': {
        'title': 'Free Furniture Background Remover - Home Decor',
        'description': 'Remove backgrounds from furniture photos. Create clean catalogs for sofas, chairs, and tables.',
        'keywords': 'furniture background remover, home decor photography, chair background removal, sofa photo editor',
        'h1': 'Clean <span class="gradient-text">Furniture Images</span>',
        'subtitle': 'Professional catalogs for your home decor business.',
        'icon': 'fa-couch',
        'features': [
            {'icon': 'fas fa-vector-square', 'title': 'Large Items', 'desc': 'Optimized for complex, large objects.'},
            {'icon': 'fas fa-palette', 'title': 'Color Accurate', 'desc': 'Maintain true fabric colors and textures.'},
            {'icon': 'fas fa-home', 'title': 'Catalog Ready', 'desc': 'Consistent look for your entire collection.'}
        ]
    },
    'animals': {
        'title': 'Free Pet Background Remover - Animal Photography',
        'description': 'Remove backgrounds from pet photos. perfect for shelters, breeders, and pet lovers.',
        'keywords': 'pet background remover, dog photo editor, cat background removal, animal photography tool',
        'h1': 'Cute <span class="gradient-text">Pet Portraits</span>',
        'subtitle': 'Highlight your furry friends without the clutter.',
        'icon': 'fa-paw',
        'features': [
            {'icon': 'fas fa-cat', 'title': 'Fur Detection', 'desc': 'Advanced AI handles fur and whiskers perfectly.'},
            {'icon': 'fas fa-heart', 'title': 'Shelter Friendly', 'desc': 'Make adoptable pets look their best.'},
            {'icon': 'fas fa-camera', 'title': 'Print Ready', 'desc': 'High resolution for framing and gifts.'}
        ]
    },
    'people': {
        'title': 'Free Portrait Background Remover - People Photography',
        'description': 'Remove backgrounds from portraits and selfies. Create professional headshots or fun stickers.',
        'keywords': 'portrait background remover, selfie editor, remove person background, headshot tool',
        'h1': 'Stunning <span class="gradient-text">Portraits</span>',
        'subtitle': 'Focus on the person, remove the distractions.',
        'icon': 'fa-user',
        'features': [
            {'icon': 'fas fa-smile', 'title': 'Face Focus', 'desc': 'Prioritizes facial features and hair details.'},
            {'icon': 'fas fa-id-card', 'title': 'ID Photos', 'desc': 'Create compliant photos for documents.'},
            {'icon': 'fas fa-users', 'title': 'Group Shots', 'desc': 'Works perfectly with multiple people.'}
        ]
    },
    'real-estate': {
        'title': 'Free Real Estate Background Remover - Property Photos',
        'description': 'Remove sky or clutter from real estate photos. enhance curb appeal for listings.',
        'keywords': 'real estate photo editor, sky replacement, property background remover, house photography',
        'h1': 'Enhance <span class="gradient-text">Property Photos</span>',
        'subtitle': 'Sell homes faster with cleaner, brighter images.',
        'icon': 'fa-home',
        'features': [
            {'icon': 'fas fa-sun', 'title': 'Sky Appeal', 'desc': 'Easily replace dull skies with blue ones.'},
            {'icon': 'fas fa-tree', 'title': 'Curb Appeal', 'desc': 'Remove unsightly objects from the yard.'},
            {'icon': 'fas fa-chart-line', 'title': 'Sell Faster', 'desc': 'Professional photos attract more buyers.'}
        ]
    },
    'graphics': {
        'title': 'Free Graphic Background Remover - Logos & Icons',
        'description': 'Turn logos and graphics into transparent PNGs. Essential for designers and marketers.',
        'keywords': 'logo background remover, transparent logo maker, icon editor, graphic design tool',
        'h1': 'Transparent <span class="gradient-text">Graphics</span>',
        'subtitle': 'Prepare logos and icons for any background.',
        'icon': 'fa-pen-nib',
        'features': [
            {'icon': 'fas fa-vector-square', 'title': 'Crisp Edges', 'desc': 'Maintains sharp lines and typography.'},
            {'icon': 'fas fa-layer-group', 'title': 'Overlay Ready', 'desc': 'Perfect for watermarks and presentations.'},
            {'icon': 'fas fa-file-image', 'title': 'Format Support', 'desc': 'Works with JPG, PNG, and WebP.'}
        ]
    },
    'signatures': {
        'title': 'Free Signature Background Remover - Digital Signatures',
        'description': 'Digitize your signature instantly. Remove paper backgrounds for a clean, transparent signature image.',
        'keywords': 'signature background remover, digital signature creator, sign PDF, transparent signature',
        'h1': 'Digital <span class="gradient-text">Signatures</span>',
        'subtitle': 'Sign documents professionally without a scanner.',
        'icon': 'fa-file-signature',
        'features': [
            {'icon': 'fas fa-pen-fancy', 'title': 'Ink Clarity', 'desc': 'Enhances contrast for legible signatures.'},
            {'icon': 'fas fa-file-contract', 'title': 'Doc Ready', 'desc': 'Drag and drop onto any PDF or Word doc.'},
            {'icon': 'fas fa-lock', 'title': 'Secure', 'desc': 'Your signature is processed locally/privately.'}
        ]
    },
    # NEW RECOMMENDED USE CASES
    'amazon': {
        'title': 'Free Amazon Product Photo Editor - White Background',
        'description': 'Create compliant Amazon product photos instantly. Pure white backgrounds for increased sales.',
        'keywords': 'amazon photo editor, amazon white background, product photography tool, ecommerce image editor',
        'h1': 'Amazon <span class="gradient-text">Product Photos</span>',
        'subtitle': 'Meet Amazon requirements instantly. Boost your CTR.',
        'icon': 'fab fa-amazon',
        'features': [
            {'icon': 'fas fa-check-circle', 'title': 'Amazon Compliant', 'desc': 'Pure white (RGB 255,255,255) backgrounds.'},
            {'icon': 'fas fa-box-open', 'title': 'Product Focus', 'desc': 'Centers your product and removes distractions.'},
            {'icon': 'fas fa-chart-bar', 'title': 'Boost Sales', 'desc': 'Professional images lead to higher conversion.'}
        ]
    },
    'shopify': {
        'title': 'Free Shopify Background Remover - Ecommerce',
        'description': 'Clean up your Shopify store images. Consistent, professional product photography in seconds.',
        'keywords': 'shopify background remover, ecommerce photo editor, online store image tool, product catalog',
        'h1': 'Professional <span class="gradient-text">Shopify Images</span>',
        'subtitle': 'Upgrade your store\'s look with consistent photography.',
        'icon': 'fab fa-shopify',
        'features': [
            {'icon': 'fas fa-camera', 'title': 'Studio Look', 'desc': 'Give your store a high-end, branded feel.'},
            {'icon': 'fas fa-sync', 'title': 'Batch Ready', 'desc': 'Process multiple product shots quickly.'},
            {'icon': 'fas fa-mobile-alt', 'title': 'Mobile Optimized', 'desc': 'Clean images load faster on mobile.'}
        ]
    },
    'ebay': {
        'title': 'Free eBay Background Remover - Reseller Tool',
        'description': 'Clean up eBay listing photos. Stand out from other sellers with professional, clutter-free images.',
        'keywords': 'ebay photo editor, reseller tool, poshmark background remover, depop photo tool',
        'h1': 'Better <span class="gradient-text">eBay Listings</span>',
        'subtitle': 'Sell your items faster with cleaner photos.',
        'icon': 'fab fa-ebay',
        'features': [
            {'icon': 'fas fa-tag', 'title': 'Stand Out', 'desc': 'Grab attention in search results.'},
            {'icon': 'fas fa-camera-retro', 'title': 'No Studio Needed', 'desc': 'Turn smartphone pics into pro listings.'},
            {'icon': 'fas fa-dollar-sign', 'title': 'Increase Value', 'desc': 'Professional photos justify higher prices.'}
        ]
    },
    'id-photo': {
        'title': 'Free Passport & ID Photo Maker - Background Remover',
        'description': 'Create compliant passport and ID photos at home. Remove backgrounds and replace with white or blue.',
        'keywords': 'passport photo maker, id photo editor, visa photo tool, background remover for id',
        'h1': 'DIY <span class="gradient-text">Passport Photos</span>',
        'subtitle': 'Save money. Create official ID photos instantly.',
        'icon': 'fas fa-id-card',
        'features': [
            {'icon': 'fas fa-globe', 'title': 'Global Standards', 'desc': 'Supports white/blue backgrounds for any country.'},
            {'icon': 'fas fa-money-bill-wave', 'title': 'Free & Fast', 'desc': 'Skip the expensive photo booth.'},
            {'icon': 'fas fa-print', 'title': 'Print Ready', 'desc': 'Download high-res for printing.'}
        ]
    },
    'profile-picture': {
        'title': 'Free Profile Picture Maker - LinkedIn & Socials',
        'description': 'Create professional profile pictures for LinkedIn, Twitter, and Instagram. Remove distractions instantly.',
        'keywords': 'profile picture maker, linkedin photo editor, headshot background remover, avatar creator',
        'h1': 'Pro <span class="gradient-text">Headshots</span>',
        'subtitle': 'Level up your personal brand on LinkedIn and social media.',
        'icon': 'fas fa-user-tie',
        'features': [
            {'icon': 'fas fa-briefcase', 'title': 'LinkedIn Ready', 'desc': 'Look professional and trustworthy.'},
            {'icon': 'fas fa-paint-brush', 'title': 'Abstract Backgrounds', 'desc': 'Add colors or gradients to match your brand.'},
            {'icon': 'fas fa-smile-beam', 'title': 'Stand Out', 'desc': 'Make a memorable first impression.'}
        ]
    },
    'logos': { # Re-adding Logos explicitly if needed, though 'graphics' covers it. Let's keep distinct.
        'title': 'Free Transparent Logo Maker - Remove White Background',
        'description': 'Make your logo transparent instantly. Remove white box backgrounds for websites, videos, and print.',
        'keywords': 'transparent logo maker, remove white background, logo editor, png logo tool',
        'h1': 'Transparent <span class="gradient-text">Logos</span>',
        'subtitle': 'Unbox your brand. Perfect for websites and headers.',
        'icon': 'fas fa-shapes',
        'features': [
            {'icon': 'fas fa-magic', 'title': 'Auto-Detect', 'desc': 'Instantly identifies logo shapes.'},
            {'icon': 'fas fa-tint-slash', 'title': 'No Halo', 'desc': 'Clean extraction without white edges.'},
            {'icon': 'fas fa-vector-square', 'title': 'Versatile', 'desc': 'Use your logo on any background.'}
        ]
    }
}

TEMPLATE_PATH = 'frontend/index.html'

def generate_page(slug, config):
    print(f"Generating page for: {slug}")
    
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # 1. Update Title
    if soup.title:
        soup.title.string = config['title']

    # 2. Update Description
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    if desc_tag:
        desc_tag['content'] = config['description']

    # 3. Update Keywords
    kw_tag = soup.find('meta', attrs={'name': 'keywords'})
    if kw_tag:
        kw_tag['content'] = config['keywords']
        
    # 4. Update OG/Twitter Tags (Optional but good for SEO)
    og_title = soup.find('meta', property='og:title')
    if og_title: og_title['content'] = config['title']
    
    og_desc = soup.find('meta', property='og:description')
    if og_desc: og_desc['content'] = config['description']
    
    og_url = soup.find('meta', property='og:url')
    if og_url: og_url['content'] = f"https://convertly.up.railway.app/{slug}.html"

    twitter_title = soup.find('meta', property='twitter:title')
    if twitter_title: twitter_title['content'] = config['title']
    
    twitter_desc = soup.find('meta', property='twitter:description')
    if twitter_desc: twitter_desc['content'] = config['description']
    
    twitter_url = soup.find('meta', property='twitter:url')
    if twitter_url: twitter_url['content'] = f"https://convertly.up.railway.app/{slug}.html"
    
    canonical = soup.find('link', rel='canonical')
    if canonical: canonical['href'] = f"https://convertly.up.railway.app/{slug}.html"

    # 5. Update Hero H1
    h1 = soup.find('h1')
    if h1:
        h1.clear()
        # Parse the HTML string for H1 (to handle spans)
        h1_soup = BeautifulSoup(config['h1'], 'html.parser')
        h1.append(h1_soup)

    # 6. Update Subtitle
    subtitle = soup.find('p', class_='subtitle')
    if subtitle:
        subtitle.clear()
        sub_soup = BeautifulSoup(config['subtitle'], 'html.parser')
        subtitle.append(sub_soup)
        
    # 7. Update Icon (Optional: in upload box)
    upload_icon = soup.find('div', class_='upload-icon').find('i')
    if upload_icon:
        upload_icon['class'] = f"fas {config.get('icon', 'fa-image')}"

    # 8. Update Features Section
    features_container = soup.find('div', class_='features')
    if features_container and 'features' in config:
        features_container.clear()
        for feature in config['features']:
            feature_html = f"""
            <div class="feature-item">
                <div class="feature-icon"><i class="{feature['icon']}"></i></div>
                <h3>{feature['title']}</h3>
                <p>{feature['desc']}</p>
            </div>
            """
            features_container.append(BeautifulSoup(feature_html, 'html.parser'))
            
    # 9. Inject Full Footer Directory (Links to all pages)
    footer_dir = soup.find('div', class_='footer-directory')
    if footer_dir:
        # We can construct the Use Cases column dynamically
        use_cases_html = '<h4>Use Cases</h4>\n'
        for k, v in USE_CASES.items():
            # Use specific link text based on title or a shorter version
            link_text = v['title'].split(' - ')[0].replace('Free ', '')
            use_cases_html += f'<a href="{k}.html">{link_text}</a>\n'
            
        # Find the column and replace content
        columns = footer_dir.find_all('div', class_='footer-column')
        if len(columns) > 1:
            # Assuming 2nd column is Use Cases (index 1) based on existing HTML
            use_case_col = columns[1]
            if use_case_col.find('h4').string == 'Use Cases':
                use_case_col.clear()
                use_case_col.append(BeautifulSoup(use_cases_html, 'html.parser'))


    # 10. CLEANUP: Remove '.seo-content' block from Template (The Background Remover text)
    # We want these pages to be clean use-case pages, not duplicated keyword stuffing.
    seo_content = soup.find('div', class_='seo-content')
    if seo_content:
        seo_content.decompose()

    # Save File
    output_path = f"frontend/{slug}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == "__main__":
    for slug, config in USE_CASES.items():
        try:
            generate_page(slug, config)
        except Exception as e:
            print(f"Error generating {slug}: {e}")
