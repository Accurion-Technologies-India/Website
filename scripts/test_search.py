import json

with open('products/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products in index: {len(products)}")

CIVIL_SYNONYMS = {
    'la': 'los angeles',
    'ctm': 'compression',
    'utm': 'universal',
    'cbr': 'bearing',
    'ndt': 'rebound'
}

def matches_item(p, query):
    q = query.lower().strip()
    specs_str = " ".join((s.get('parameter', '') + ' ' + s.get('value', '')) for s in p.get('specifications', []))
    full = " ".join([p.get('name', ''), p.get('code', ''), p.get('short_description', ''), p.get('category', ''), specs_str]).lower().replace('×', 'x')
    norm_full = "".join(c for c in full if c.isalnum())

    tokens = [t for t in q.replace('×', 'x').split() if t]
    for token in tokens:
        matched = False
        if token in full:
            matched = True
        elif token in CIVIL_SYNONYMS and CIVIL_SYNONYMS[token] in full:
            matched = True
        else:
            norm_token = "".join(c for c in token if c.isalnum())
            if norm_token and norm_token in norm_full:
                matched = True
        if not matched:
            return False
    return True

queries = ['slump', 'vicat', 'cbr', 'cube mould', '100x100', 'penetration', 'la abrasion', 'balance', 'chemical', 'anvil', 'sieve', 'ctm 2000kn']
for q in queries:
    matches = [p['name'] for p in products if matches_item(p, q)]
    print(f"Query '{q}': {len(matches)} matches found -> {matches[:2]}")
