#!/usr/bin/env python3
import re
from pathlib import Path

html_dir = Path("public")
desc_count = {}

# Count descriptions
for html_file in html_dir.glob("*.html"):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    desc_match = re.search(r'name="description" content="([^"]+)"', content)
    if not desc_match:
        continue
    
    desc = desc_match.group(1)
    if desc not in desc_count:
        desc_count[desc] = []
    desc_count[desc].append(str(html_file))

# Fix duplicates
count = 0
for desc, files in desc_count.items():
    if len(files) > 1:
        for filepath in files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = Path(filepath).stem.replace('-', ' ')
            new_desc = f"{desc.rstrip('.')}. Variante: {filename}"[:160]
            
            new_content = re.sub(
                r'name="description" content="[^"]*"',
                f'name="description" content="{new_desc}"',
                content
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            count += 1
            print(f"Fixed: {Path(filepath).name}")

print(f"\nTotal descriptions fixed: {count}")
