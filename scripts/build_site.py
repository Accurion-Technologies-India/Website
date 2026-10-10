#!/usr/bin/env python3
"""
Accurion Technologies — Static Site Generator (Option B Builder)
Compiles structured CMS JSON data into pre-rendered, 100% static HTML pages,
updates the products.json search index, and refreshes sitemap.xml.
"""

import os
import json
import html
import re
import datetime
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
SITE_URL = "https://www.accuriontechnologies.com"

TODAY_STR = datetime.date.today().isoformat()

def markdown_to_html(md_text):
    if not md_text:
        return ""
    # Simple, safe markdown converter for paragraphs, bold, italic, and lists
    text = html.escape(md_text)
    # Bold **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic *text*
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Line breaks and paragraphs
    paragraphs = text.split("\n\n")
    html_parts = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith("- ") or p.startswith("* "):
            lines = p.split("\n")
            list_items = "".join([f"<li>{l.lstrip('-* ')}</li>" for l in lines if l.strip()])
            html_parts.append(f"<ul>{list_items}</ul>")
        elif p.startswith("### "):
            html_parts.append(f"<h3>{p[4:]}</h3>")
        elif p.startswith("## "):
            html_parts.append(f"<h2>{p[3:]}</h2>")
        else:
            p = p.replace("\n", "<br />")
            html_parts.append(f"<p>{p}</p>")
    return "\n".join(html_parts)

def load_data():
    categories = {}
    cat_dir = os.path.join(DATA_DIR, "categories")
    if os.path.isdir(cat_dir):
        for f in os.listdir(cat_dir):
            if f.endswith(".json"):
                with open(os.path.join(cat_dir, f), "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    categories[data["slug"]] = data

    products = []
    prod_dir = os.path.join(DATA_DIR, "products")
    if os.path.isdir(prod_dir):
        for f in os.listdir(prod_dir):
            if f.endswith(".json"):
                with open(os.path.join(prod_dir, f), "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    products.append(data)

    blogs = []
    blog_dir = os.path.join(DATA_DIR, "blogs")
    if os.path.isdir(blog_dir):
        for f in os.listdir(blog_dir):
            if f.endswith(".json"):
                with open(os.path.join(blog_dir, f), "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    blogs.append(data)

    settings = {}
    sett_dir = os.path.join(DATA_DIR, "settings")
    for s_name in ["company", "homepage", "theme"]:
        s_path = os.path.join(sett_dir, f"{s_name}.json")
        if os.path.isfile(s_path):
            with open(s_path, "r", encoding="utf-8") as fp:
                settings[s_name] = json.load(fp)

    return categories, products, blogs, settings

def render_product_page(prod, cat_data, all_prods_in_cat):
    cat_name = cat_data.get("name", "Products") if cat_data else "Products"
    cat_slug = cat_data.get("slug", "products") if cat_data else "products"
    prod_name = prod.get("name", "Product")
    prod_code = prod.get("code", "")
    prod_slug = prod.get("slug", "")
    short_desc = prod.get("short_description", "")
    full_desc_md = prod.get("description", "")
    full_desc_html = markdown_to_html(full_desc_md)
    featured_img = prod.get("featured_image", "/images/products/ndt/langry-rh225a-mech.jpg")
    gallery = prod.get("gallery", [])
    key_features = prod.get("key_features", [])
    specs = prod.get("specifications", [])
    brochure = prod.get("brochure", "")
    seo_title = prod.get("seo_title") or f"{prod_name} | Accurion Technologies"
    seo_desc = prod.get("seo_description") or short_desc
    canonical_url = f"{SITE_URL}/products/{cat_slug}/{prod_slug}/"

    # Schema JSON-LD
    schema_product = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": prod_name,
        "sku": prod_code,
        "image": f"{SITE_URL}{featured_img}" if featured_img.startswith("/") else featured_img,
        "description": short_desc,
        "category": cat_name,
        "brand": {
            "@type": "Brand",
            "name": "Accurion Technologies"
        },
        "offers": {
            "@type": "Offer",
            "priceCurrency": "INR",
            "availability": "https://schema.org/InStock",
            "url": f"{canonical_url}#enquire"
        }
    }

    schema_breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            { "@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/" },
            { "@type": "ListItem", "position": 2, "name": "Products", "item": f"{SITE_URL}/products/" },
            { "@type": "ListItem", "position": 3, "name": cat_name, "item": f"{SITE_URL}/products/{cat_slug}/" },
            { "@type": "ListItem", "position": 4, "name": prod_name, "item": canonical_url }
        ]
    }

    # Specifications Table Rows
    specs_html_rows = []
    for s in specs:
        p = html.escape(str(s.get("parameter", "")))
        v = html.escape(str(s.get("value", "")))
        specs_html_rows.append(f"""<tr>
          <td style="padding:12px 18px;font-weight:600;color:var(--color-text-secondary);width:40%;border-bottom:1px solid var(--color-border);">{p}</td>
          <td style="padding:12px 18px;font-weight:600;color:var(--color-text);border-bottom:1px solid var(--color-border);">{v}</td>
        </tr>""")
    specs_table_body = "\n".join(specs_html_rows)

    # Key Features List Items
    features_html_items = []
    for f in key_features:
        feat = html.escape(str(f.get("feature", "")))
        features_html_items.append(f"""<li style="display:flex;align-items:flex-start;gap:10px;margin-bottom:8px;font-size:0.95rem;color:var(--color-text);">
          <span style="color:var(--color-success, #16a34a);font-weight:bold;font-size:1.1rem;line-height:1;">✓</span>
          <span>{feat}</span>
        </li>""")
    features_list_html = "\n".join(features_html_items)

    # Brochure Action Button
    brochure_btn_html = ""
    if brochure:
        brochure_btn_html = f"""<a href="{brochure}" target="_blank" rel="noopener" class="btn btn-outline" style="display:inline-flex;align-items:center;gap:8px;padding:12px 22px;">
          <span>📄</span> Download Datasheet PDF
        </a>"""

    # Related Products from same category
    related_html_cards = []
    for r in all_prods_in_cat:
        if r.get("slug") == prod_slug or r.get("status") != "published":
            continue
        r_name = html.escape(r.get("name", ""))
        r_code = html.escape(r.get("code", ""))
        r_img = r.get("featured_image", "")
        r_slug = r.get("slug", "")
        r_short = html.escape(r.get("short_description", "")[:120]) + "..."
        related_html_cards.append(f"""
        <div class="product-card">
          <div class="product-card-img-wrap">
            <img src="{r_img}" alt="{r_name}" class="product-card-img" width="300" height="200" loading="lazy" />
          </div>
          <div class="product-card-body">
            <div class="product-model-tag">Model {r_code}</div>
            <h3>{r_name}</h3>
            <p>{r_short}</p>
            <a href="products/{cat_slug}/{r_slug}/" class="btn btn-outline" style="margin-top:auto;width:100%;justify-content:center;">View Details →</a>
          </div>
        </div>
        """)
    related_cards_html = "\n".join(related_html_cards[:3])

    page_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <base href="/" />
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(seo_title)}</title>
  <meta name="description" content="{html.escape(seo_desc)}" />
  <link rel="canonical" href="{canonical_url}" />
  <meta property="og:title" content="{html.escape(seo_title)}" />
  <meta property="og:description" content="{html.escape(seo_desc)}" />
  <meta property="og:image" content="{SITE_URL}{featured_img if featured_img.startswith('/') else '/' + featured_img}" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:type" content="product" />
  <meta property="og:site_name" content="Accurion Technologies" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(seo_title)}" />
  <meta name="twitter:description" content="{html.escape(seo_desc)}" />
  <meta name="twitter:image" content="{SITE_URL}{featured_img if featured_img.startswith('/') else '/' + featured_img}" />
  <link rel="icon" href="favicon.ico" sizes="48x48" />
  <link rel="icon" href="assets/logo/favicon-32x32.png" type="image/png" sizes="32x32" />
  <link rel="apple-touch-icon" href="assets/logo/apple-touch-icon.png" sizes="180x180" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&amp;display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/style.css" />
  <script>!function(){{var t=localStorage.getItem("accurion-theme")||((window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches)?"dark":"light");document.documentElement.setAttribute("data-theme",t)}}();</script>
  <script type="application/ld+json">
{json.dumps(schema_product, indent=2, ensure_ascii=False)}
  </script>
  <script type="application/ld+json">
{json.dumps(schema_breadcrumbs, indent=2, ensure_ascii=False)}
  </script>
</head>
<body data-page="products">
  <a class="skip-link" href="#main-content">Skip to Content</a>
  <main id="main-content">

    <!-- Page Header / Breadcrumb -->
    <section class="page-hero" style="padding: 38px 0 34px;">
      <div class="container">
        <div class="page-hero-content">
          <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="./">Home</a><span class="breadcrumb-sep">›</span>
            <a href="products/">Products</a><span class="breadcrumb-sep">›</span>
            <a href="products/{cat_slug}/">{html.escape(cat_name)}</a><span class="breadcrumb-sep">›</span>
            <span>{html.escape(prod_code or prod_name)}</span>
          </nav>
          <div style="display:flex;align-items:center;gap:12px;margin-top:14px;flex-wrap:wrap;">
            <span class="product-badge badge-popular" style="position:static;font-size:0.8rem;">{html.escape(cat_name)}</span>
            <span style="font-size:0.85rem;color:rgba(255,255,255,0.8);font-weight:600;">Model: {html.escape(prod_code)}</span>
          </div>
          <h1 style="font-size:clamp(1.7rem, 3.2vw, 2.6rem);margin-top:8px;">{html.escape(prod_name)}</h1>
        </div>
      </div>
    </section>

    <!-- Product Showcase Split Section -->
    <section class="section" style="padding-top:40px;">
      <div class="container">
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));gap:48px;align-items:start;">

          <!-- Left Column: Smart Image Canvas -->
          <div>
            <div class="smart-image-canvas" style="height:380px;border:1px solid var(--color-border);border-radius:var(--radius-lg);box-shadow:var(--shadow-md);">
              <div class="ambient-backdrop" style="background-image:url('{featured_img}');"></div>
              <img src="{featured_img}" alt="{html.escape(prod_name)}" class="foreground-instrument" style="max-height:330px;" />
            </div>
            <div style="margin-top:14px;font-size:0.82rem;color:var(--color-text-secondary);text-align:center;">
              Official equipment supplied by Accurion Technologies &bull; Calibration verified
            </div>
          </div>

          <!-- Right Column: Quick Overview & Actions -->
          <div>
            <div class="product-model-tag" style="font-size:0.88rem;color:var(--color-primary);font-weight:700;margin-bottom:10px;">
              Accurion Equipment Catalogue &bull; SKU {html.escape(prod_code)}
            </div>
            <p style="font-size:1.08rem;line-height:1.65;color:var(--color-text);margin-bottom:24px;">
              {html.escape(short_desc)}
            </p>

            <!-- Key Features Repeater -->
            <div style="background:var(--color-surface);border:1px solid var(--color-border);border-radius:var(--radius-md);padding:20px;margin-bottom:28px;">
              <h3 style="font-size:1rem;font-weight:700;margin-bottom:14px;text-transform:uppercase;letter-spacing:0.04em;color:var(--color-text);">Key Engineering Highlights</h3>
              <ul style="list-style:none;padding:0;margin:0;">
                {features_list_html}
              </ul>
            </div>

            <!-- Action CTAs -->
            <div id="enquire" style="display:flex;gap:14px;flex-wrap:wrap;align-items:center;">
              <a href="contact?product={html.escape(prod_name)}" class="btn btn-primary" style="padding:14px 28px;font-size:1rem;font-weight:700;">
                Request Official Quote
              </a>
              {brochure_btn_html}
            </div>
          </div>

        </div>

        <!-- Technical Description Section -->
        <div style="margin-top:64px;border-top:1px solid var(--color-border);padding-top:48px;">
          <h2 style="font-size:1.6rem;font-weight:800;margin-bottom:20px;">Technical Overview &amp; Compliance</h2>
          <div style="font-size:1.02rem;line-height:1.8;color:var(--color-text-secondary);max-width:920px;">
            {full_desc_html}
          </div>
        </div>

        <!-- Technical Specifications Table -->
        <div style="margin-top:48px;">
          <h2 style="font-size:1.6rem;font-weight:800;margin-bottom:20px;">Verified Technical Specifications</h2>
          <div style="overflow-x:auto;background:var(--color-card-bg);border:1px solid var(--color-border);border-radius:var(--radius-lg);box-shadow:var(--shadow-sm);max-width:880px;">
            <table style="width:100%;border-collapse:collapse;font-size:0.92rem;text-align:left;">
              <thead>
                <tr style="background:var(--color-surface);border-bottom:2px solid var(--color-border);">
                  <th style="padding:14px 18px;font-weight:700;">Parameter</th>
                  <th style="padding:14px 18px;font-weight:700;">Specification Value</th>
                </tr>
              </thead>
              <tbody>
                {specs_table_body}
              </tbody>
            </table>
          </div>
        </div>

        <!-- Related Equipment in Category -->
        {"<div style='margin-top:64px;border-top:1px solid var(--color-border);padding-top:48px;'><h2 style='font-size:1.5rem;font-weight:800;margin-bottom:24px;'>Related " + html.escape(cat_name) + "</h2><div class='product-grid'>" + related_cards_html + "</div></div>" if related_cards_html else ""}

      </div>
    </section>

  </main>
  <script src="js/components.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
"""
    return page_html

def generate_products_json(published_products):
    search_index = []
    for p in published_products:
        search_index.append({
            "name": p.get("name", ""),
            "code": p.get("code", ""),
            "slug": p.get("slug", ""),
            "category": p.get("category", ""),
            "subcategory": p.get("subcategory", ""),
            "short_description": p.get("short_description", ""),
            "featured_image": p.get("featured_image", ""),
            "url": f"products/{p.get('category', '')}/{p.get('slug', '')}/",
            "featured": p.get("featured", False),
            "display_order": p.get("display_order", 10),
            "specifications": p.get("specifications", [])
        })
    out_path = os.path.join(ROOT_DIR, "products", "products.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(search_index, f, indent=2, ensure_ascii=False)
    print(f"Generated search index at: products/products.json ({len(search_index)} items)")

def update_sitemap(published_products, categories, blogs):
    sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")

    # Static baseline pages
    core_urls = [
        {"loc": f"{SITE_URL}/", "priority": "1.0", "changefreq": "weekly"},
        {"loc": f"{SITE_URL}/about/", "priority": "0.8", "changefreq": "monthly"},
        {"loc": f"{SITE_URL}/services/", "priority": "0.9", "changefreq": "monthly"},
        {"loc": f"{SITE_URL}/products/", "priority": "0.9", "changefreq": "weekly"},
        {"loc": f"{SITE_URL}/blogs/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{SITE_URL}/contact/", "priority": "0.9", "changefreq": "monthly"},
        {"loc": f"{SITE_URL}/privacy/", "priority": "0.3", "changefreq": "yearly"},
        {"loc": f"{SITE_URL}/terms/", "priority": "0.3", "changefreq": "yearly"},
    ]

    # Category URLs
    for cat_slug in categories:
        core_urls.append({
            "loc": f"{SITE_URL}/products/{cat_slug}/",
            "priority": "0.8",
            "changefreq": "weekly"
        })

    # Blog URLs
    for b in blogs:
        b_slug = b.get("slug", "")
        core_urls.append({
            "loc": f"{SITE_URL}/blog/{b_slug}/",
            "priority": "0.8",
            "changefreq": "monthly"
        })

    # Product URLs
    for p in published_products:
        cat_slug = p.get("category", "")
        p_slug = p.get("slug", "")
        core_urls.append({
            "loc": f"{SITE_URL}/products/{cat_slug}/{p_slug}/",
            "priority": "0.85",
            "changefreq": "monthly"
        })

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for u in core_urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{u['loc']}</loc>")
        xml_lines.append(f"    <lastmod>{TODAY_STR}</lastmod>")
        xml_lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{u['priority']}</priority>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>")

    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines) + "\n")
    print(f"Updated sitemap.xml with {len(core_urls)} indexed URLs")

def build_site():
    print("=" * 60)
    print("Accurion Technologies — Static Site Builder Engine")
    print("=" * 60)

    categories, products, blogs, settings = load_data()
    print(f"Loaded: {len(categories)} categories, {len(products)} products, {len(blogs)} blogs")

    # Filter published products
    published_products = [p for p in products if p.get("status") == "published"]
    print(f"Published Products: {len(published_products)} of {len(products)}")

    # 1. Compile individual product pages
    compiled_count = 0
    for prod in published_products:
        cat_slug = prod.get("category", "")
        prod_slug = prod.get("slug", "")
        cat_data = categories.get(cat_slug)
        all_cat_prods = [p for p in published_products if p.get("category") == cat_slug]

        page_content = render_product_page(prod, cat_data, all_cat_prods)

        target_dir = os.path.join(ROOT_DIR, "products", cat_slug, prod_slug)
        os.makedirs(target_dir, exist_ok=True)
        target_file = os.path.join(target_dir, "index.html")

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(page_content)
        compiled_count += 1
        print(f"  ✓ Compiled product: products/{cat_slug}/{prod_slug}/index.html")

    # 2. Generate search index products.json
    generate_products_json(published_products)

    # 3. Update sitemap.xml
    update_sitemap(published_products, categories, blogs)

    print("=" * 60)
    print(f"Build complete! Successfully generated {compiled_count} product pages.")
    print("=" * 60)

if __name__ == "__main__":
    build_site()
