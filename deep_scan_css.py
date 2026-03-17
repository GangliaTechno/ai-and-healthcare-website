
import re
import os

def deep_scan_css():
    files = [
        r"p:\AI-website-clone\node_site\public\assets\css\style.css",
        r"p:\AI-website-clone\node_site\public\assets\css\index.css",
        r"p:\AI-website-clone\node_site\public\assets\css\responsive.css"
    ]
    
    # Keywords to search in selectors
    selector_keywords = ['apply', 'cta', 'faq', 'highlight', 'btn', 'button']
    # Properties to search
    prop_keywords = ['linear-gradient', 'radial-gradient', 'background', 'border']
    
    print("--- Deep Scan CSS ---")
    
    for file_path in files:
        if not os.path.exists(file_path):
            continue
        
        print(f"\nScanning {os.path.basename(file_path)}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Basic block parser (very simple, assumes good formatting or just finds lines)
        # Using regex to find blocks might be better.
        
        # Let's just iterate lines for simplicity and grep-like context
        lines = content.split('\n')
        in_block = False
        current_selector = ""
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Check for selector
            if '{' in line:
                current_selector = line.split('{')[0].strip()
                in_block = True
            
            if '}' in line:
                in_block = False
                current_selector = ""
            
            # Check if selector matches context
            selector_match = any(k in current_selector.lower() for k in selector_keywords) if current_selector else False
            
            # Check for properties
            prop_match = any(k in line_stripped.lower() for k in prop_keywords)
            
            if selector_match or (prop_match and ('gradient' in line_stripped.lower() or 'red' in line_stripped.lower())):
                 # Filter checks to avoid noise
                 if 'transparent' in line_stripped.lower() and 'gradient' in line_stripped.lower() and '#fff' in line_stripped:
                     continue # Skip the white filter gradient seen previously if it's just white
                 
                 print(f"[{i+1}] {line_stripped}  <-- {current_selector}")

if __name__ == "__main__":
    deep_scan_css()
