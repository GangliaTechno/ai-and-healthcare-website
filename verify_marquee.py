import os
import re

def verify_marquee_links(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    continue
                
                if '<div class="marquee-container">' in content:
                    print(f"\nFile: {file}")
                    # Extract the marquee block
                    match = re.search(r'<div class="marquee-container">([\s\S]*?)</div>', content)
                    if match:
                        block = match.group(1)
                        # Find the a tag
                        a_match = re.search(r'<a\s+[^>]*>', block)
                        if a_match:
                            print(f"  Link: {a_match.group(0)}")
                            if 'href="javascript:void(0)"' in a_match.group(0) \
                               and 'data-open="enquiry-modal"' in a_match.group(0) \
                               and 'apply-now-btn' in a_match.group(0) \
                               and 'target="_blank"' not in a_match.group(0):
                                print("  [OK] Correct attributes.")
                            else:
                                print("  [FAIL] Incorrect attributes.")
                        else:
                            print("  [INFO] No link tag found in marquee container.")
                    else:
                         print("  [WARN] Regex failed to extract marquee block.")

verify_marquee_links(r"p:\AI-website-clone\node_site\public")
