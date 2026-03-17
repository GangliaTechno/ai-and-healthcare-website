import os
import re

def scan_html_files(directory):
    files_to_check = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                files_to_check.append(os.path.join(root, file))
    
    print(f"Scanning {len(files_to_check)} files...")
    
    for file_path in files_to_check:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find marquee container
        marquee_matches = re.finditer(r'<div class="marquee-container">([\s\S]*?)</div>', content)
        
        found_marquee = False
        needs_fix = False
        
        for match in marquee_matches:
            found_marquee = True
            marquee_block = match.group(1)
            
            # Check for links inside marquee
            link_matches = re.finditer(r'<a\s+([^>]*)>', marquee_block)
            for link_match in link_matches:
                attrs = link_match.group(1)
                
                # Check for criteria
                if 'href="javascript:void(0)"' not in attrs:
                    needs_fix = True
                    print(f"[NEEDS FIX] {file_path}: href not javascript:void(0)")
                if 'data-open="enquiry-modal"' not in attrs:
                    needs_fix = True
                    print(f"[NEEDS FIX] {file_path}: missing data-open")
                if 'apply-now-btn' not in attrs:
                    needs_fix = True
                    print(f"[NEEDS FIX] {file_path}: missing class apply-now-btn")
                if 'target="_blank"' in attrs:
                    needs_fix = True
                    print(f"[NEEDS FIX] {file_path}: has target=_blank")

scan_html_files(r"p:\AI-website-clone\node_site\public")
