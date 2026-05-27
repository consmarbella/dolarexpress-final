#!/bin/bash
# Find files with duplicate titles and add file-specific suffix
declare -A title_files
for file in public/*.html; do
  title=$(grep -o '<title>[^<]*</title>' "$file" | sed 's/<[^>]*>//g')
  if [ ! -z "$title" ]; then
    base_title="${title% | DolarExpress}"
    if [[ "${title_files[$base_title]}" == *"$file"* ]]; then
      # Duplicate found, add filename hint
      filename=$(basename "$file" .html | sed 's/-/ /g')
      new_title="$base_title • $filename | DolarExpress"
      new_title_esc=$(echo "$new_title" | sed 's/[\/&]/\&/g')
      sed -i "s|<title>.*</title>|<title>$new_title_esc</title>|" "$file"
    else
      title_files["$base_title"]+="$file "
    fi
  fi
done
echo "✓ Duplicate titles made unique"
