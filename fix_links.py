import os
import re
import glob

# Pattern to find the specific anchor tag
# Matches <a ... href="..." ...>
# We capture the whole tag to process it
tag_pattern = re.compile(r'(<a\s+[^>]*?href=["\']https://set2026\.ishinfosys\.com/SYM20-SET26/apply/Index\.aspx["\'][^>]*?>)', re.IGNORECASE)

def process_tag(match):
    tag = match.group(1)
    
    # 1. Neutralize Href
    # Replace the specific href with javascript:void(0)
    tag = re.sub(r'href=["\']https://set2026\.ishinfosys\.com/SYM20-SET26/apply/Index\.aspx["\']', 'href="javascript:void(0)"', tag, flags=re.IGNORECASE)
    
    # 2. Add data-open
    if 'data-open=' not in tag:
        # Insert after <a 
        tag = tag.replace('<a ', '<a data-open="enquiry-modal" ', 1)
        
    # 3. Handle Class
    if 'class=' in tag:
        # Check if apply-now-btn is already there
        if 'apply-now-btn' not in tag:
            # Append to existing class using regex to find the content inside quotes
            tag = re.sub(r'class=(["\'])(.*?)\1', r'class=\1\2 apply-now-btn\1', tag, count=1)
    else:
        # Add new class
        tag = tag.replace('<a ', '<a class="apply-now-btn" ', 1)
        
    # 4. Remove target="_blank"
    tag = re.sub(r'\s*target=["\']_blank["\']', '', tag, flags=re.IGNORECASE)
    
    return tag

files = glob.glob('p:/AI-website-clone/node_site/public/**/*.html', recursive=True)
count = 0

for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = tag_pattern.sub(process_tag, content)
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {fpath}")
            count += 1
    except Exception as e:
        print(f"Error processing {fpath}: {e}")

print(f"Finished. Updated {count} files.")
