#!/usr/bin/env python3
import os
import re
from pathlib import Path

html_dir = Path("public")
title_count = {}

for html_file in html_dir.glob("*.html"):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'<title>([^<]+)</title>', content)
    if not title_match:
        continue
    
    title = title_match.group(1)
    base_title = title.replace(" | DolarExpress", "").strip()
    
    if base_title not in title_count:
        title_count[base_title] = []
    title_count[base_title].append(str(html_file))

for base_title, files in title_count.items():
    if len(files) > 1:
        for filepath in files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = Path(filepath).stem.replace('-', ' ').title()
            new_title = f"{base_title} • {filename} | DolarExpress"
            
            new_content = re.sub(
                r'<title>[^<]+</title>',
                f'<title>{new_title}</title>',
                content
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"Fixed: {Path(filepath).name}")

print(f"\nTotal unique base titles: {len(title_count)}")
