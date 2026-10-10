# Accurion Technologies — Client CMS Quick Start Cheatsheet
*A non-technical, step-by-step executive guide for managing equipment, quotations, and content on your website.*

---

## 🚀 Quick Access Links

| Portal | URL / Destination | Purpose |
| :--- | :--- | :--- |
| **Admin CMS** | `/admin/` | Manage Equipment, Categories, Services, Blogs & Settings |
| **Enquiries CRM** | `/admin/enquiries/` | Review Leads, Manage Quotations & Send 1-Click WhatsApps |
| **Public Catalogue** | `/products/` | Instant Search & Filter Equipment by IS Standard / Model |
| **Live Website** | `https://www.accuriontechnologies.com/` | Public Facing Storefront & Portal |

---

## ⏱️ How to Add a New Instrument in Under 3 Minutes

Follow these 6 simple steps to add and publish any testing instrument to your live website:

### Step 1: Open the Equipment Catalogue
1. Navigate to `/admin/` in your browser.
2. Click **Login with GitHub** (or click *Preview Dashboard in Sandbox Mode* for offline testing).
3. In the left sidebar, click **Equipment Catalogue**.
4. Click the blue **New Equipment** button at the top right.

### Step 2: Fill in Commercial Information
* **Product Name**: Type the full commercial title (e.g. `Langry RH225-B Integrated Digital Rebound Hammer`).
* **Product Code / SKU**: Enter the model code (e.g. `RH225-B` or `ACC-CTM-2000D`).
* **URL Slug**: Autocompletes or enter lowercase letters with hyphens (e.g. `langry-rh225b-integrated-digital-rebound-hammer`).
* **Category**: Select the primary discipline from the dropdown (e.g. `NDT Equipment`, `Concrete Testing Equipment`, `Compression Testing Machines`).
* **Subcategory**: Specific testing group (e.g. `Rebound Hammers`).
* **Short Description**: 1–2 crisp sentences for catalogue cards and Google search previews.

### Step 3: Add Image & Media (Zero Image Worry!)
* **Featured Image**: Click **Choose an image** and upload from your computer or phone.
  > 🛡️ **Zero-Crop Guarantee**: Our built-in **4-Layer Image Defense** automatically centers your instrument on a professional studio canvas, prevents awkward edge cutoffs, auto-rotates phone photos, and compresses to high-speed WebP (< 150 KB).

### Step 4: Add Technical Specifications (Repeater)
Under **Technical Specifications**, click **+ Add specification**:
* **Parameter**: e.g. `Impact Energy` | **Value**: `2.207 J`
* **Parameter**: e.g. `Measuring Range` | **Value**: `10 to 60 MPa`
* **Parameter**: e.g. `Applicable Standards` | **Value**: `IS 13311 (Part 2), ASTM C805, EN 12504-2`
* Click **+ Add specification** to add as many rows as needed.

### Step 5: Key Features & PDF Datasheet
* Under **Key Features**, add 3 to 6 bullet points highlighting core benefits (e.g. *Integrated OLED display*, *Wireless Bluetooth printer connection*, *Type-C USB rechargeable lithium battery*).
* (Optional) Under **Datasheet / Brochure PDF**, upload your official PDF brochure for 1-click customer downloads.

### Step 6: Publish!
1. Check that **Publication Status** is set to `Published (Visible on Website)`.
2. Inspect the **Live Card Preview** on the right side of the split screen to confirm how it looks.
3. Click the green **Publish** button at the top right.
4. **Done!** The automated GitHub Actions build engine will pre-render the 100% static HTML page, index the model for instant search, and update Google sitemaps automatically.

---

## 📋 Managing Customer Enquiries & Quotations

Navigate to `/admin/enquiries/` to manage leads submitted through your website:

1. **Review Incoming Inquiries**:
   - Inquiries appear immediately with date, customer name, company, and equipment requested (e.g. *Langry RH225-B*).
2. **Instant 1-Click WhatsApp**:
   - Click the green **💬 WA** button next to any enquiry to open WhatsApp Web or App with a courteous, pre-populated greeting referencing their specific instrument inquiry.
3. **Update Status**:
   - Use the status dropdown on each row to track progress:
     - `⚡ New`: Fresh lead awaiting initial call.
     - `📞 Contacted`: Customer spoken to / requirements discussed.
     - `📑 Quoted`: Formal commercial proposal sent.
     - `🏆 Closed`: Deal won / order dispatched.
4. **Export for Accounting & Sales**:
   - Click **📥 Export CSV** to download all records into an Excel-ready spreadsheet.
5. **Log Offline Calls**:
   - Click **+ Log New Enquiry** to record walk-in customers or phone calls in one centralized CRM.

---

## 🛠️ Managing Services & Brand Settings

* **Services Management**:
  - Open **Services** in the sidebar to update descriptions, standards, and scope for:
    - *NABL Accredited Calibration Services*
    - *Complete Civil Quality Lab Setup*
    - *Repair & Maintenance of Lab Equipment*
* **Site & Brand Settings**:
  - Open **Site & Brand Settings** to update your phone number, WhatsApp contact number, GSTIN, office address, or hero banner headline without editing code.

---

## ❓ Frequently Asked Questions (FAQ)

### Q: Will my website go down if GitHub has an issue?
**No.** Your public website is 100% pre-rendered static HTML hosted globally on fast CDN edges. The CMS is an administrative management layer that compiles changes into static files; your website will never crash or slow down.

### Q: What if an image uploaded by staff is the wrong aspect ratio?
Our **4-Layer Image Defense** automatically applies `object-fit: contain` with an intelligent studio-neutral canvas and ambient blur backdrop. Your instruments will **never** be stretched, distorted, or cropped at the edges.

### Q: Can I save an instrument as a draft without making it live?
**Yes.** Change the **Publication Status** dropdown from `Published` to `Draft (Saved Internally)`. It will remain securely stored in your CMS without appearing on the public catalogue.

### Q: How do customers search for equipment?
Visitors can visit `/products/` and type any keyword, model number (e.g. `RH225-B`), capacity (e.g. `2000 kN`), or standard (e.g. `IS 13311`) to see instant filtered results in real-time.

---
*Accurion Technologies — Precision Civil Quality Testing Solutions across India.*
