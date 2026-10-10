#!/usr/bin/env python3
import os
import sys
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pages_checked = 0
issues = []

for root, dirs, files in os.walk(ROOT):
    if any(d in root for d in ['.git', '__pycache__', '.tempmediaStorage', '.agents', '.gemini', 'admin']):
        continue
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            rel = os.path.relpath(path, ROOT).replace('\\', '/')
            pages_checked += 1
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                soup = BeautifulSoup(fp.read(), 'html.parser')
            
            # Check og:image
            og_img = soup.find('meta', property='og:image')
            if og_img:
                img_url = og_img.get('content', '')
                if img_url.startswith('https://www.accuriontechnologies.com/'):
                    local_img = img_url.replace('https://www.accuriontechnologies.com/', '')
                    if not os.path.exists(os.path.join(ROOT, local_img)):
                        issues.append((rel, f"Broken og:image: {img_url}"))
            
            # Check favicon
            icon = soup.find('link', rel=lambda r: r and 'icon' in r)
            if not icon:
                issues.append((rel, "Missing favicon link"))

            # Check json-ld
            json_lds = soup.find_all('script', type='application/ld+json')
            if not json_lds and rel not in ['404.html', 'privacy/index.html', 'terms/index.html']:
                issues.append((rel, "Missing JSON-LD structured data"))

print(f"Checked {pages_checked} public pages.")
print(f"Total issues found: {len(issues)}")
for r, msg in issues[:15]:
    print(f"  - [{r}] {msg}")
