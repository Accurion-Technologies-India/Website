#!/usr/bin/env python3
"""
Accurion Technologies — CMS Data Architecture Validator
Validates JSON schemas, data types, and referential integrity across all content models.
"""

import os
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def load_json(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f), None
    except Exception as e:
        return None, str(e)

def validate_categories():
    cat_dir = os.path.join(DATA_DIR, "categories")
    if not os.path.isdir(cat_dir):
        return {}, [f"Categories directory missing at {cat_dir}"]
    
    categories = {}
    errors = []
    
    required_fields = ["name", "slug", "description", "display_order"]
    
    for filename in os.listdir(cat_dir):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(cat_dir, filename)
        data, err = load_json(filepath)
        if err:
            errors.append(f"Invalid JSON in {filename}: {err}")
            continue
        
        # Check required fields
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f"Category {filename} missing required field '{field}'")
        
        # Validate slug
        slug = data.get("slug", "")
        if not SLUG_PATTERN.match(slug):
            errors.append(f"Category {filename} has invalid slug format: '{slug}'")
        if f"{slug}.json" != filename:
            errors.append(f"Category filename '{filename}' does not match slug '{slug}'")
            
        categories[slug] = data
        
    return categories, errors

def validate_products(valid_categories):
    prod_dir = os.path.join(DATA_DIR, "products")
    if not os.path.isdir(prod_dir):
        return [], [f"Products directory missing at {prod_dir}"]
    
    products = []
    errors = []
    
    required_fields = [
        "name", "code", "slug", "category", "status",
        "short_description", "description", "featured_image",
        "key_features", "specifications"
    ]
    
    for filename in os.listdir(prod_dir):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(prod_dir, filename)
        data, err = load_json(filepath)
        if err:
            errors.append(f"Invalid JSON in {filename}: {err}")
            continue
        
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f"Product {filename} missing required field '{field}'")
        
        # Validate slug
        slug = data.get("slug", "")
        if not SLUG_PATTERN.match(slug):
            errors.append(f"Product {filename} has invalid slug format: '{slug}'")
            
        # Check category reference
        cat_ref = data.get("category", "")
        if cat_ref not in valid_categories:
            errors.append(f"Product {filename} references unknown category '{cat_ref}'")
            
        # Validate specifications structure
        specs = data.get("specifications", [])
        if not isinstance(specs, list):
            errors.append(f"Product {filename} 'specifications' must be a list")
        else:
            for i, spec in enumerate(specs):
                if not isinstance(spec, dict) or "parameter" not in spec or "value" not in spec:
                    errors.append(f"Product {filename} spec #{i} invalid format (needs parameter, value)")
                    
        # Validate key features structure
        features = data.get("key_features", [])
        if not isinstance(features, list):
            errors.append(f"Product {filename} 'key_features' must be a list")
        else:
            for i, feat in enumerate(features):
                if not isinstance(feat, dict) or "feature" not in feat:
                    errors.append(f"Product {filename} feature #{i} invalid format (needs feature string)")
                    
        # Validate status
        status = data.get("status")
        if status not in ["published", "draft", "archived"]:
            errors.append(f"Product {filename} invalid status: '{status}'")
            
        products.append(data)
        
    return products, errors

def validate_blogs():
    blog_dir = os.path.join(DATA_DIR, "blogs")
    if not os.path.isdir(blog_dir):
        return [], [f"Blogs directory missing at {blog_dir}"]
    
    blogs = []
    errors = []
    required_fields = ["title", "slug", "date", "author", "featured_image", "excerpt", "body"]
    
    for filename in os.listdir(blog_dir):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(blog_dir, filename)
        data, err = load_json(filepath)
        if err:
            errors.append(f"Invalid JSON in {filename}: {err}")
            continue
        
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f"Blog {filename} missing required field '{field}'")
                
        slug = data.get("slug", "")
        if not SLUG_PATTERN.match(slug):
            errors.append(f"Blog {filename} has invalid slug format: '{slug}'")
            
        blogs.append(data)
        
    return blogs, errors

def validate_settings():
    settings_dir = os.path.join(DATA_DIR, "settings")
    errors = []
    
    # 1. Company
    company_path = os.path.join(settings_dir, "company.json")
    if not os.path.isfile(company_path):
        errors.append("Missing data/settings/company.json")
    else:
        data, err = load_json(company_path)
        if err:
            errors.append(f"Invalid company.json: {err}")
        else:
            for f in ["name", "phone", "whatsapp", "email", "address", "gstin", "logo"]:
                if f not in data or not data[f]:
                    errors.append(f"company.json missing field '{f}'")
                    
    # 2. Homepage
    hp_path = os.path.join(settings_dir, "homepage.json")
    if not os.path.isfile(hp_path):
        errors.append("Missing data/settings/homepage.json")
    else:
        data, err = load_json(hp_path)
        if err:
            errors.append(f"Invalid homepage.json: {err}")
        else:
            for f in ["hero_title", "hero_subtitle", "hero_image", "hero_cta_text", "hero_cta_link"]:
                if f not in data or not data[f]:
                    errors.append(f"homepage.json missing field '{f}'")
                    
    # 3. Theme
    theme_path = os.path.join(settings_dir, "theme.json")
    if not os.path.isfile(theme_path):
        errors.append("Missing data/settings/theme.json")
    else:
        data, err = load_json(theme_path)
        if err:
            errors.append(f"Invalid theme.json: {err}")
        else:
            for f in ["primary_color", "primary_dark_color", "font_family"]:
                if f not in data or not data[f]:
                    errors.append(f"theme.json missing field '{f}'")
                    
    return errors

def validate_services():
    serv_dir = os.path.join(DATA_DIR, "services")
    if not os.path.isdir(serv_dir):
        return [], [f"Services directory missing at {serv_dir}"]
    
    services = []
    errors = []
    required_fields = ["title", "service_number", "slug", "short_description", "full_description", "features", "display_order"]
    
    for filename in os.listdir(serv_dir):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(serv_dir, filename)
        data, err = load_json(filepath)
        if err:
            errors.append(f"Invalid JSON in {filename}: {err}")
            continue
        
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f"Service {filename} missing required field '{field}'")
                
        slug = data.get("slug", "")
        if not SLUG_PATTERN.match(slug):
            errors.append(f"Service {filename} has invalid slug format: '{slug}'")
        if f"{slug}.json" != filename:
            errors.append(f"Service filename '{filename}' does not match slug '{slug}'")
            
        services.append(data)
        
    return services, errors

def main():
    print("=" * 60)
    print("Accurion Technologies — Validating Content Architecture")
    print("=" * 60)
    
    all_errors = []
    
    categories, cat_errors = validate_categories()
    all_errors.extend(cat_errors)
    print(f"Categories: {len(categories)} valid files checked")
    
    products, prod_errors = validate_products(categories)
    all_errors.extend(prod_errors)
    print(f"Products:   {len(products)} valid files checked")
    
    blogs, blog_errors = validate_blogs()
    all_errors.extend(blog_errors)
    print(f"Blogs:      {len(blogs)} valid files checked")

    services, serv_errors = validate_services()
    all_errors.extend(serv_errors)
    print(f"Services:   {len(services)} valid files checked")
    
    sett_errors = validate_settings()
    all_errors.extend(sett_errors)
    print(f"Settings:   Checked company.json, homepage.json, theme.json")
    
    print("-" * 60)
    if all_errors:
        print(f"Validation FAILED with {len(all_errors)} errors:")
        for err in all_errors:
            print(f"  ❌ {err}")
        sys.exit(1)
    else:
        print("Validation PASSED! 100% of data models and references are valid.")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    main()
