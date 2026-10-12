# Accurion Technologies — Project Memory & Architecture Guide

> **Primary Purpose:** High-density reference for AI assistants and developers to eliminate repetitive repository exploration, reduce token consumption, and maintain strict architectural consistency.

---

## 1. System Philosophy & Strict Constraints

| Rule | Specification |
|---|---|
| **Tech Stack** | **Vanilla HTML5, Vanilla CSS, Vanilla JavaScript** (ES6+). |
| **Build Tools** | **NO npm / Vite / webpack build steps.** No Tailwind CSS. No React/Vue. |
| **Static SSG Engine** | Python scripts in `scripts/build_site.py` compile `data/products/*.json` into pre-rendered static HTML. |
| **Hosting & DNS** | **GitHub Pages** with custom domain `www.accuriontechnologies.com` via `CNAME` file. `.nojekyll` enabled. |
| **Repository** | `Accurion-Technologies-India/Website` (`main` branch). |
| **CI/CD Automation** | `.github/workflows/build-and-deploy.yml` triggers on push to `main`, runs data validators, image processors, and site compiler, and pushes static HTML directly. |
| **Path Strategy** | Root-relative or base-href compatible paths (`/css/style.css`, `/images/`, `products/`). |

---

## 2. Brand Identity & Design Tokens

### Color Tokens (CSS Variables)
* **Primary Accent:** `#C41217` (Dark mode: `#E8353B`)
* **Background:** Light `#FFFFFF` | Dark `#0F0F0F`
* **Surface/Cards:** Light `#F5F5F5` | Dark `#1A1A1A`
* **Text Primary:** Light `#111111` | Dark `#F0F0F0`
* **Text Secondary:** Light `#555555` | Dark `#9A9A9A`
* **Borders:** Light `#E0E0E0` | Dark `#2A2A2A`
* **Theme Persistence:** Key `accurion-theme` (`light` | `dark`) in `localStorage`. Attribute: `data-theme` on `<html>`.

### Typography
* **Font Family:** `'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
* **Tagline:** *"Where Accuracy Meets Innovation"*

---

## 3. Directory Map & Routing

* `index.html`: Homepage featuring ambient hero carousel, category cards, feature grid, and trust stats.
* `products/`: Master catalogue page with real-time client-side live search and category pill filters.
* `products/{category}/`: 17 category portals (e.g. `ndt-equipment/`, `soil-testing/`, `cement-testing/`, etc.).
* `products/{category}/{slug}/`: Individual product pages compiled from `data/products/*.json`.
* `admin/`: Decap CMS portal (`admin/index.html`, `admin/config.yml`, `admin/cms-theme.css`, `admin/enquiries/`).
* `js/main.js`: Main interactive logic (mobile navigation, theme toggle, hero slider, instant search).
* `js/components.js`: Shared reusable components (navbar, footer, WhatsApp floating widget).
* `scripts/`: Python utility scripts (`build_site.py`, `compile_all_products.py`, `process_images.py`, `validate_data.py`).

---

## 4. Product Data Schema (`data/products/*.json` & `products/products.json`)

Each product entry adheres to:
```json
{
  "name": "Product Display Name",
  "code": "MODEL-123",
  "slug": "product-display-name",
  "category": "category-slug",
  "subcategory": "subcategory-slug",
  "status": "published",
  "short_description": "1-2 sentence overview for cards and meta description",
  "description": "Full markdown-supported description",
  "featured_image": "/images/products/category/product-image.webp",
  "gallery_images": [],
  "standards": ["IS 5514", "ASTM C191", "EN 196-3"],
  "specifications": [
    { "label": "Plunger Diameter", "value": "10 mm" },
    { "label": "Needle Diameter", "value": "1.13 mm" }
  ],
  "featured": false
}
```

---

## 5. Partner Sourcing Guidelines
* **NDT Equipment:** Official partner brand is **Langry** (`langryndt.com`). Models: RH225-A, RH225-B, RH450-A, RH550-A, RH75-A, RH20-A, RS150/250/350, UPV2100.
* **Water Testing:** Official partner brand is **Aquasol** (`aquasol.co.in`).
* **Civil Lab Equipment:** Governed by Bureau of Indian Standards (BIS / IS codes) and ASTM standards.
* **Pricing Policy:** **Strictly NO pricing** displayed. All quotation requests route through the website contact form (`/contact/?product={Name}&code={Code}`).
