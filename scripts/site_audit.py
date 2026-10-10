#!/usr/bin/env python3
"""
Accurion Technologies — Comprehensive Website Auditor
Scans every HTML file, JSON data asset, image reference, link, and SEO tag
to detect broken links, 404 images, missing metadata, and unoptimized assets.
"""

import os
import re
import json
import urllib.parse
import sys
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_audit():
    print("=" * 70)
    print("ACCURION TECHNOLOGIES — FULL SITE AUDIT REPORT")
    print("=" * 70)

    html_files = []
    for root, dirs, files in os.walk(ROOT_DIR):
        # Ignore git, cache, temp, and node_modules if any
        if any(d in root for d in ['.git', '__pycache__', '.tempmediaStorage', '.agents', '.gemini']):
            continue
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))

    print(f"Total HTML pages discovered: {len(html_files)}")

    broken_links = []
    broken_images = []
    broken_scripts = []
    broken_styles = []
    seo_issues = []
    missing_alts = []
    multiple_h1 = []
    missing_h1 = []

    for file_path in html_files:
        rel_path = os.path.relpath(file_path, ROOT_DIR).replace('\\', '/')
        if rel_path.startswith('admin/'):
            # Admin single-page app handles routing dynamically
            continue

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')
        except Exception as e:
            print(f"Error reading {rel_path}: {e}")
            continue

        base_tag = soup.find('base')
        base_href = base_tag.get('href') if base_tag else None

        # 1. SEO Checks
        title = soup.find('title')
        if not title or not title.get_text().strip():
            seo_issues.append((rel_path, "Missing or empty <title> tag"))

        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc or not meta_desc.get('content', '').strip():
            seo_issues.append((rel_path, "Missing or empty <meta name='description'>"))

        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if not canonical or not canonical.get('href', '').strip():
            seo_issues.append((rel_path, "Missing canonical <link rel='canonical'>"))

        h1s = soup.find_all('h1')
        if len(h1s) == 0:
            missing_h1.append(rel_path)
        elif len(h1s) > 1:
            multiple_h1.append((rel_path, len(h1s)))

        # 2. Image verification
        imgs = soup.find_all('img')
        for img in imgs:
            src = img.get('src')
            alt = img.get('alt')
            if alt is None:
                missing_alts.append((rel_path, src or 'no-src'))

            if not src or src.startswith('http') or src.startswith('data:') or src.startswith('//'):
                continue

            clean_src = src.split('?')[0].split('#')[0]
            if clean_src.startswith('/'):
                target_disk = os.path.join(ROOT_DIR, clean_src.lstrip('/'))
            elif base_href == '/':
                target_disk = os.path.join(ROOT_DIR, clean_src)
            else:
                target_disk = os.path.join(os.path.dirname(file_path), clean_src)

            target_disk = os.path.normpath(target_disk)
            if not os.path.exists(target_disk):
                broken_images.append((rel_path, src, target_disk))

        # 3. CSS Link verification
        css_links = soup.find_all('link', attrs={'rel': 'stylesheet'})
        for link in css_links:
            href = link.get('href')
            if not href or href.startswith('http') or href.startswith('//'):
                continue
            clean_href = href.split('?')[0].split('#')[0]
            if clean_href.startswith('/'):
                target_disk = os.path.join(ROOT_DIR, clean_href.lstrip('/'))
            elif base_href == '/':
                target_disk = os.path.join(ROOT_DIR, clean_href)
            else:
                target_disk = os.path.join(os.path.dirname(file_path), clean_href)
            target_disk = os.path.normpath(target_disk)
            if not os.path.exists(target_disk):
                broken_styles.append((rel_path, href))

        # 4. Script verification
        scripts = soup.find_all('script', src=True)
        for s in scripts:
            src = s.get('src')
            if not src or src.startswith('http') or src.startswith('//'):
                continue
            clean_src = src.split('?')[0].split('#')[0]
            if clean_src.startswith('/'):
                target_disk = os.path.join(ROOT_DIR, clean_src.lstrip('/'))
            elif base_href == '/':
                target_disk = os.path.join(ROOT_DIR, clean_src)
            else:
                target_disk = os.path.join(os.path.dirname(file_path), clean_src)
            target_disk = os.path.normpath(target_disk)
            if not os.path.exists(target_disk):
                broken_scripts.append((rel_path, src))

        # 5. Anchor link verification
        anchors = soup.find_all('a', href=True)
        for a in anchors:
            href = a.get('href')
            if not href:
                continue
            # Ignore external, anchor-only, tel, mailto, whatsapp
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:', '#')):
                continue

            clean_href = href.split('?')[0].split('#')[0]
            if not clean_href or clean_href == '/':
                continue

            # Determine disk path
            if clean_href.startswith('/'):
                test_path = clean_href.lstrip('/')
            elif base_href == '/':
                test_path = clean_href
            else:
                dir_rel = os.path.relpath(os.path.dirname(file_path), ROOT_DIR).replace('\\', '/')
                if dir_rel == '.':
                    test_path = clean_href
                else:
                    test_path = f"{dir_rel}/{clean_href}"

            test_path = urllib.parse.unquote(test_path)
            cand1 = os.path.normpath(os.path.join(ROOT_DIR, test_path))
            cand2 = os.path.normpath(os.path.join(ROOT_DIR, test_path, "index.html"))
            cand3 = os.path.normpath(os.path.join(ROOT_DIR, test_path + ".html"))

            if not (os.path.exists(cand1) or os.path.exists(cand2) or os.path.exists(cand3)):
                # Filter known special or root relative fallbacks
                broken_links.append((rel_path, href, test_path))

    # 6. Audit Products Search Index
    print("\nAuditing products/products.json:")
    prod_json_path = os.path.join(ROOT_DIR, 'products', 'products.json')
    broken_prod_images = []
    empty_prod_fields = []
    if os.path.exists(prod_json_path):
        with open(prod_json_path, 'r', encoding='utf-8') as f:
            prods = json.load(f)
            print(f"Total products in index: {len(prods)}")
            for p in prods:
                img = p.get('featured_image', '')
                if img and not img.startswith('http'):
                    clean_img = img.lstrip('/')
                    if not os.path.exists(os.path.join(ROOT_DIR, clean_img)):
                        broken_prod_images.append((p.get('name'), img))
                if not p.get('name') or not p.get('category'):
                    empty_prod_fields.append(p)

    # 7. Audit Sitemap.xml
    print("Auditing sitemap.xml:")
    sitemap_path = os.path.join(ROOT_DIR, 'sitemap.xml')
    broken_sitemap_urls = []
    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            sm_content = f.read()
            urls = re.findall(r'<loc>https://www\.accuriontechnologies\.com/([^<]*)</loc>', sm_content)
            for u in urls:
                cand1 = os.path.normpath(os.path.join(ROOT_DIR, u))
                cand2 = os.path.normpath(os.path.join(ROOT_DIR, u, "index.html"))
                cand3 = os.path.normpath(os.path.join(ROOT_DIR, u.rstrip('/') + ".html"))
                if not (os.path.exists(cand1) or os.path.exists(cand2) or os.path.exists(cand3)):
                    broken_sitemap_urls.append(u)

    # 8. Report Results
    print("\n" + "=" * 70)
    print("AUDIT FINDINGS SUMMARY")
    print("=" * 70)

    print(f"❌ Broken Images:           {len(broken_images)}")
    for r, src, _ in broken_images[:10]:
        print(f"   - In [{r}]: {src}")

    print(f"❌ Broken Internal Links:    {len(broken_links)}")
    for r, href, _ in broken_links[:10]:
        print(f"   - In [{r}]: href='{href}'")

    print(f"❌ Broken Scripts:           {len(broken_scripts)}")
    for r, s in broken_scripts:
        print(f"   - In [{r}]: {s}")

    print(f"❌ Broken Stylesheets:       {len(broken_styles)}")
    for r, st in broken_styles:
        print(f"   - In [{r}]: {st}")

    print(f"❌ Missing Image Alt tags:   {len(missing_alts)}")
    for r, src in missing_alts[:5]:
        print(f"   - In [{r}]: img src='{src}' has no alt")

    print(f"⚠️  SEO Missing Tags:        {len(seo_issues)}")
    for r, issue in seo_issues[:10]:
        print(f"   - In [{r}]: {issue}")

    print(f"⚠️  Missing H1:               {len(missing_h1)}")
    for r in missing_h1:
        print(f"   - [{r}] has no <h1>")

    print(f"⚠️  Multiple H1:              {len(multiple_h1)}")
    for r, c in multiple_h1:
        print(f"   - [{r}] has {c} <h1> tags")

    print(f"❌ Broken Product JSON Imgs: {len(broken_prod_images)}")
    for name, img in broken_prod_images[:10]:
        print(f"   - Product '{name}': {img} not on disk")

    print(f"❌ Broken Sitemap URLs:      {len(broken_sitemap_urls)}")
    for u in broken_sitemap_urls:
        print(f"   - sitemap URL: /{u}")

    print("=" * 70)

if __name__ == '__main__':
    run_audit()
