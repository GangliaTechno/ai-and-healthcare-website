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
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find marquee container
        # We process the file content by finding the marquee block and replacing it
        
        def replace_marquee_link(match):
            block = match.group(0) # The full marquee container block
            
            # Pattern for the link inside: <a href="...?" ...> ... </a>
            # We want to be careful not to match nested divs too aggressively if regex is simple
            # But the structure is usually: <div class="marquee-container"> <a ...> <div class="marquee-content"> ... </div> </a> </div>
            
            # Let's find the <a> tag
            # We look for <a ...> followed by <div class="marquee-content">
            
            def link_replacer(link_match):
                original_tag = link_match.group(0)
                # Extract inner content if needed, but we just want to replace the opening tag
                
                # Check if it is the link wrapping marquee-content
                # The regex below ensures we match <a ...> before <div class="marquee-content">
                
                # Construct new tag
                return '<a class="apply-now-btn" data-open="enquiry-modal" href="javascript:void(0)">'

            # Regex to find the specific anchor tag that wraps marquee-content
            # <a [^>]*>\s*<div class="marquee-content"
            
            new_block = re.sub(r'<a\s+[^>]*>(?=\s*<div class="marquee-content")', link_replacer, block)
            
            # Also need to remove target="_blank" if it was there (replaced by whole new tag above)
            # The above replacement REPLACES the whole opening <a> tag, so it effectively removes old href and target.
            
            return new_block

        # Apply replacement to marquee containers
        new_content = re.sub(r'<div class="marquee-container">([\s\S]*?)</div>', replace_marquee_link, content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed: {file_path}")
            fixed_count += 1

    print(f"Total files fixed: {fixed_count}")

fix_marquee_links(r"p:\AI-website-clone\node_site\public")
