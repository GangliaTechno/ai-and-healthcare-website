import os
import re

public_dir = r"p:\AI-website-clone\node_site\public"
index_path = os.path.join(public_dir, "index.html")

# Read index.html to extract the announcement bar
with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

# Extract the announcement bar
# It's an element <div class="announcebar-wp" id="mahe-announcement-bar"> ... </div>
# We can use regex to find this entire div, assuming it ends before <header class="sticky">
announce_match = re.search(r'(<div class="announcebar-wp" id="mahe-announcement-bar">.*?)<header class="sticky">', index_html, flags=re.DOTALL)

if not announce_match:
    print("Could not find the announcement bar in index.html")
    exit(1)

announce_html = announce_match.group(1).strip() + "\n  "

# Now loop through all other html files
for filename in os.listdir(public_dir):
    if filename.endswith(".html") and filename != "index.html":
        filepath = os.path.join(public_dir, filename)
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            encoding_used = "utf-8"
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="latin-1") as f:
                content = f.read()
            encoding_used = "latin-1"
            
        # Check if it already has the announcement bar
        if "id=\"mahe-announcement-bar\"" in content or "announcebar-wp" in content:
            # If it does, we might want to replace it to ensure it's up to date
            content = re.sub(r'<div class="announcebar-wp".*?</div>\s*(?=<header)', '', content, flags=re.DOTALL)
            
        # Insert before <header class="sticky">
        header_match = re.search(r'<header class="sticky">', content)
        if header_match:
            new_content = content[:header_match.start()] + announce_html + content[header_match.start():]
            
            with open(filepath, "w", encoding=encoding_used) as f:
                f.write(new_content)
            print(f"Added announcement bar to {filename} (encoding: {encoding_used})")
        else:
            print(f"Skipped {filename}: <header class=\"sticky\"> not found")

print("Done inserting announcement bar.")
