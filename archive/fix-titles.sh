#!/bin/bash
for file in public/*.html; do
  # Get the H1 text
  h1=$(grep -oP '(?<=<h1[^>]*>).*?(?=</h1>)' "$file" | sed 's/<[^>]*>//g' | head -1)
  
  if [ ! -z "$h1" ]; then
    # Create new title from H1
    new_title="$h1 | DolarExpress"
    # Escape special chars for sed
    new_title_escaped=$(printf '%s\n' "$new_title" | sed -e 's/[\/&]/\&/g')
    
    # Replace title tag
    sed -i "s|<title>.*</title>|<title>$new_title_escaped</title>|" "$file"
  fi
done
echo "✓ Titles updated from H1 content"
