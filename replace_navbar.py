import os
import re

public_dir = r"p:\AI-website-clone\node_site\public"
index_path = os.path.join(public_dir, "index.html")

with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

# Extract the header block
header_match = re.search(r'<header[^>]*>.*?</header>', index_html, flags=re.DOTALL)
if not header_match:
    print("Could not find <header> in index.html")
    exit(1)

new_header = header_match.group(0)

# Replace in all other HTML files
for filename in os.listdir(public_dir):
    if filename.endswith(".html") and filename != "index.html":
        filepath = os.path.join(public_dir, filename)
        
        # Try reading with utf-8, fallback to latin-1
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            encoding_used = "utf-8"
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="latin-1") as f:
                content = f.read()
            encoding_used = "latin-1"
            
        old_header_match = re.search(r'<header[^>]*>.*?</header>', content, flags=re.DOTALL)
        if old_header_match:
            new_content = content[:old_header_match.start()] + new_header + content[old_header_match.end():]
            
            # Write back the new content
            with open(filepath, "w", encoding=encoding_used) as f:
                f.write(new_content)
            print(f"Updated {filename} (encoding: {encoding_used})")
        else:
            print(f"No header found in {filename}")

print("Navbar replacement complete.")
