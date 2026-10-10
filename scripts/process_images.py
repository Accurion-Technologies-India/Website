#!/usr/bin/env python3
"""
Accurion Technologies — 4-Layer Image Defense Processing Pipeline
Auto-compresses uploaded client equipment photos:
- Fixes smartphone EXIF orientation
- Caps maximum dimensions to 1200px
- Converts/compresses to razor-sharp WebP under 150 KB
- Converts CMYK/RGBA safely to RGB/sRGB
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from PIL import Image, ImageOps

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "uploads")
MAX_DIMENSION = 1200
TARGET_MAX_BYTES = 150 * 1024  # 150 KB
DEFAULT_WEBP_QUALITY = 82

def optimize_image(filepath):
    filename = os.path.basename(filepath)
    if filename.startswith(".") or filename.endswith(".gitkeep"):
        return None

    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"]:
        return None

    original_size = os.path.getsize(filepath)

    try:
        with Image.open(filepath) as img:
            # 1. Layer 3a: Auto-rotate based on EXIF tag (phone cameras)
            img = ImageOps.exif_transpose(img)

            # 2. Layer 3b: Color mode normalization
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                # Preserve transparency for PNG/WebP if transparent
                has_alpha = True
            else:
                has_alpha = False
                if img.mode != "RGB":
                    img = img.convert("RGB")

            # 3. Layer 3c: Dimension capping (max 1200px)
            width, height = img.size
            if width > MAX_DIMENSION or height > MAX_DIMENSION:
                if width > height:
                    new_w = MAX_DIMENSION
                    new_h = int(height * (MAX_DIMENSION / width))
                else:
                    new_h = MAX_DIMENSION
                    new_w = int(width * (MAX_DIMENSION / height))
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

            # 4. Layer 3d: Target WebP compilation
            base_name = os.path.splitext(filepath)[0]
            webp_path = f"{base_name}.webp"

            quality = DEFAULT_WEBP_QUALITY
            # Try saving WebP
            img.save(webp_path, format="WEBP", quality=quality, method=6)
            new_size = os.path.getsize(webp_path)

            # If still larger than 150KB, reduce quality iteratively
            while new_size > TARGET_MAX_BYTES and quality > 45:
                quality -= 8
                img.save(webp_path, format="WEBP", quality=quality, method=6)
                new_size = os.path.getsize(webp_path)

            savings = ((original_size - new_size) / original_size) * 100 if original_size > 0 else 0
            return {
                "file": filename,
                "original_kb": round(original_size / 1024, 1),
                "optimized_kb": round(new_size / 1024, 1),
                "savings_pct": round(savings, 1),
                "dimensions": f"{img.size[0]}x{img.size[1]}",
                "webp_file": os.path.basename(webp_path)
            }

    except Exception as e:
        print(f"  ⚠️ Error processing {filename}: {e}", file=sys.stderr)
        return None

def process_all_uploads():
    if not os.path.isdir(UPLOAD_DIR):
        print(f"Directory {UPLOAD_DIR} does not exist. Skipping.")
        return

    print("=" * 60)
    print("Accurion Technologies — Processing Uploaded Media (4-Layer Defense)")
    print(f"Scanning: {UPLOAD_DIR}")
    print("=" * 60)

    count = 0
    total_orig = 0
    total_opt = 0

    for root, _, files in os.walk(UPLOAD_DIR):
        for f in files:
            filepath = os.path.join(root, f)
            # Only process non-webp or original uploads
            if f.endswith(".webp") and os.path.exists(os.path.join(root, f.replace(".webp", ".jpg"))):
                continue
            
            stats = optimize_image(filepath)
            if stats:
                count += 1
                total_orig += stats["original_kb"]
                total_opt += stats["optimized_kb"]
                print(f"  ✓ {stats['file']}: {stats['original_kb']} KB -> {stats['optimized_kb']} KB WebP [{stats['dimensions']}] ({stats['savings_pct']}% smaller)")

    if count == 0:
        print("  ℹ️ No unprocessed uploads found in images/uploads/")
    else:
        net_savings = ((total_orig - total_opt) / total_orig) * 100 if total_orig > 0 else 0
        print("-" * 60)
        print(f"Processed {count} images. Total: {round(total_orig, 1)} KB -> {round(total_opt, 1)} KB ({round(net_savings, 1)}% savings)")
    print("=" * 60)

if __name__ == "__main__":
    process_all_uploads()
