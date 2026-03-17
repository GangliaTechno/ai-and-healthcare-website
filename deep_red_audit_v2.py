
import os
import re

def deep_red_audit_v2():
    base_dir = r"p:\AI-website-clone\node_site\public"
    
    known_bads = [
        '#9e181d', '#bf2617', '#b01116', '#af251c',
        '#c4161c', '#c2272c', '#ff4d4d', '#b20000',
        'red', 'crimson', 'maroon', 'firebrick', 'tomato', 'darkred'
    ]
    
    print("--- Scanning for Red Assets & Styles (No JS) ---")

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            fpath = os.path.join(root, file)
            
            # Skip JS
            if file.endswith('.js'): continue
            
            # 1. SVGs
            if file.endswith('.svg'):
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                suspects = []
                if '#ff0000' in content.lower(): suspects.append('#ff0000')
                for bad in known_bads:
                    if bad.lower() in content.lower():
                        suspects.append(bad)
                
                if suspects:
                    msg = f"[SVG] {file}: Found {suspects}"
                    print(msg)
                    with open("audit_results.txt", "a", encoding="utf-8") as out:
                        out.write(msg + "\n")

            # 2. HTML/CSS
            elif file.endswith(('.html', '.css')):
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                except:
                    continue

                for i, line in enumerate(lines):
                    lower_line = line.lower()
                    found = []
                    
                    for bad in known_bads:
                        if bad.startswith('#'):
                            if bad.lower() in lower_line:
                                found.append(bad)
                        else:
                            # Strict word boundary for color names
                            if re.search(r'\b' + re.escape(bad) + r'\b', lower_line):
                                found.append(bad)
                    
                    if '#ff0000' in lower_line: found.append('#ff0000')
                    
                    if found:
                        msg = f"[{file}:{i+1}] found {found} -> {line.strip()[:80]}"
                        print(msg)
                        with open("audit_results.txt", "a", encoding="utf-8") as out:
                            out.write(msg + "\n")

if __name__ == "__main__":
    if os.path.exists("audit_results.txt"): os.remove("audit_results.txt")
    deep_red_audit_v2()
