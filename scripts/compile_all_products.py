#!/usr/bin/env python3
"""
Accurion Technologies — Complete Catalogue Extractor & Search Index Compiler
Scans all 17 category pages and subcategories, combines them with CMS seed models,
and generates the complete products/products.json search index (120+ products).
"""

import os
import glob
import re
import json
from bs4 import BeautifulSoup

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def build_complete_catalogue():
    products_json_path = os.path.join(ROOT_DIR, 'products', 'products.json')
    
    seen_names = set()
    all_products = []

    # 1. Load existing detailed CMS seed products first (highest priority)
    if os.path.exists(products_json_path):
        with open(products_json_path, 'r', encoding='utf-8') as f:
            try:
                existing_json = json.load(f)
                for p in existing_json:
                    name = clean_text(p.get('name', ''))
                    if name and name.lower() not in seen_names:
                        seen_names.add(name.lower())
                        all_products.append(p)
            except Exception as e:
                print(f"Warning reading existing products.json: {e}")

    # 2. Scan all category & subcategory HTML pages
    pattern1 = os.path.join(ROOT_DIR, 'products', '*', 'index.html')
    pattern2 = os.path.join(ROOT_DIR, 'products', '*', '*', 'index.html')
    html_files = sorted(glob.glob(pattern1) + glob.glob(pattern2))

    for hf in html_files:
        rel = os.path.relpath(hf, ROOT_DIR).replace('\\', '/')
        parts = rel.split('/')
        # ['products', 'concrete-testing', 'index.html'] or ['products', 'ndt-equipment', 'rebound-hammers', 'index.html']
        if len(parts) < 3:
            continue
        cat_slug = parts[1]
        subcat_slug = parts[2] if len(parts) > 3 and not parts[2].endswith('.html') else ''

        # Skip individual product subpages that are already indexed
        if len(parts) > 3 and os.path.basename(os.path.dirname(hf)) in [p.get('slug', '') for p in all_products]:
            continue

        try:
            with open(hf, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
        except Exception as e:
            print(f"Error parsing {hf}: {e}")
            continue

        cards = soup.find_all('div', class_='product-card')
        for card in cards:
            h3 = card.find('h3')
            if not h3:
                continue
            name = clean_text(h3.get_text())
            if not name or name.lower() in seen_names:
                continue

            p = card.find('p')
            desc = clean_text(p.get_text()) if p else ''

            img = card.find('img')
            img_src = img.get('src') if img else ''
            if img_src and not img_src.startswith('/') and not img_src.startswith('http'):
                img_src = '/' + img_src

            tag = card.find('div', class_='product-model-tag')
            tag_text = clean_text(tag.get_text()) if tag else ''

            link = card.find('a', href=True)
            slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            
            if link and not link['href'].startswith('contact'):
                url = link['href']
            else:
                if subcat_slug:
                    url = f"products/{cat_slug}/{subcat_slug}/#{slug}"
                else:
                    url = f"products/{cat_slug}/#{slug}"

            # Specs
            specs = []
            ul = card.find('ul')
            if ul:
                for li in ul.find_all('li'):
                    text = clean_text(li.get_text())
                    if ':' in text:
                        k, v = text.split(':', 1)
                        specs.append({'parameter': clean_text(k), 'value': clean_text(v)})
                    elif text:
                        specs.append({'parameter': 'Specification', 'value': text})

            # Code / SKU
            code = ""
            if tag_text:
                code = tag_text.replace('Model', '').replace('•', '').replace('&bull;', '').strip()
            else:
                m = re.search(r'([A-Z0-9\-]{2,15}(?:kN|J|mm)?)', name)
                if m:
                    code = m.group(1)

            item = {
                'name': name,
                'code': code or tag_text,
                'slug': slug,
                'category': cat_slug,
                'subcategory': subcat_slug,
                'short_description': desc,
                'featured_image': img_src,
                'url': url,
                'featured': False,
                'specifications': specs
            }
            seen_names.add(name.lower())
            all_products.append(item)

    # Sort products alphabetically by name
    all_products.sort(key=lambda x: (x.get('category', ''), x.get('name', '')))

    # Write output to products/products.json
    with open(products_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)

    print(f"Indexed {len(all_products)} products across all categories into {products_json_path}")
    return all_products

if __name__ == '__main__':
    build_complete_catalogue()
