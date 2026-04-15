import re

# Define a function to fix URLs

def fix_urls(html_content):
    # Regex patterns to find canonical, og:url, and related links
    # This pattern finds URLs that do not end with '.html' and adds it.
    patterns = [
        (r'(<link rel="canonical" href=")[^"]*?([^/]*)(?<!\.html)(\s*"/>)', '\1\2.html\3'),
        (r'(<meta property="og:url" content=")[^"]*?([^/]*)(?<!\.html)(\s*"/>)', '\1\2.html\3'),
        (r'(<a href=")[^"]*?([^/]*)(?<!\.html)(\s*")', '\1\2.html\3'),
        (r'(footer[^>]*>\s*<a href=")[^"]*?([^/]*)(?<!\.html)(\s*")', '\1\2.html\3'),
    ]

    for pattern, replacement in patterns:
        html_content = re.sub(pattern, replacement, html_content)

    return html_content

# Example usage

# Assuming `html` is the content of your HTML document:
# fixed_html = fix_urls(html)
