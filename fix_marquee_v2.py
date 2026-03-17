import os
import re

def fix_marquee_links(directory):
    files_to_check = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                files_to_check.append(os.path.join(root, file))
    
    fixed_count = 0
    
    for file_path in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception as e:
                print(f"Skipping {file_path}: {e}")
                continue

        # Find marquee container
        def replace_marquee_link(match):
            block = match.group(0)
            
            def link_replacer(link_match):
                return '<a class="apply-now-btn" data-open="enquiry-modal" href="javascript:void(0)">'

            # Regex to find the specific anchor tag that wraps marquee-content
            new_block = re.sub(r'<a\s+[^>]*>(?=\s*<div class="marquee-content")', link_replacer, block)
            
            return new_block

        # Apply replacement to marquee containers
        new_content = re.sub(r'<div class="marquee-container">([\s\S]*?)</div>', replace_marquee_link, content)
        
        if new_content != content:
            # Write back with utf-8 to standardize
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed: {file_path}")
            fixed_count += 1
        else:
            # Debug: check if file HAS marquee but was not changed (maybe already correct?)
            if '<div class="marquee-container">' in content:
                # Check if it has marquee-content inside
                 if 'class="marquee-content"' in content:
                    # Check if the link is already correct
                    if '<a class="apply-now-btn" data-open="enquiry-modal" href="javascript:void(0)">' in content:
                        print(f"Already correct: {file_path}")
                    else:
                        print(f"Marquee found but regex failed/not matching in: {file_path}")

    print(f"Total files fixed: {fixed_count}")

fix_marquee_links(r"p:\AI-website-clone\node_site\public")
