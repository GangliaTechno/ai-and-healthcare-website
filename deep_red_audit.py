
import os
import re

def deep_red_audit():
    base_dir = r"p:\AI-website-clone\node_site\public"
    
    # Red-ish hex pattern: Starts with #9, #a, #b, #c, #d, #f followed by low values?
    # Actually, simpler to just list the known offenders found previously and generic red names.
    # User mentioned: #c4161c (old red), #AF251C, #b20000 (dark red).
    # Let's search for generic red high byte > A and G/B < 8? 
    # Regex for #RRGGBB: #[9a-fA-F][0-9a-fA-F][0-5][0-9a-fA-F][0-5][0-9a-fA-F] ? 
    # That might call orange red. safely just look for known bads and keywords.
    
    known_bads = [
        '#9e181d', '#bf2617', '#b01116', '#af251c', # Previous finds
        '#c4161c', '#c2272c', '#ff4d4d', '#b20000', # Previous/Common
        '#d1491e', # The dark orange I just added is OK (#d1491e is deep orange). 
                   # Wait, #d1491e is actually fine as a hover for #E85626, but let's just be careful.
        'red', 'crimson', 'maroon', 'firebrick', 'tomato', 'darkred'
    ]
    
    # Exclude our approved orange hover if needed, but #d1491e is arguably orange-red. 
    # User said "ZERO visible red tones". #d1491e (RGB 209, 73, 30) is strong orange-red. 
    # Only block explicitly red things.

    print("--- Scanning for Red Assets & Styles ---")

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            fpath = os.path.join(root, file)
            
            # 1. Image Assets (SVG only)
            if file.endswith('.svg'):
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for fills/strokes in hex or rgb
                # Simple check for the known bads or pure red #ff0000
                suspects = []
                if '#ff0000' in content.lower(): suspects.append('#ff0000')
                for bad in known_bads:
                    if bad.lower() in content.lower():
                        suspects.append(bad)
                
                if suspects:
                    print(f"[SVG] Found {suspects} in {file}")

            # 2. Code files (HTML, CSS)
            elif file.endswith(('.html', '.css', '.js')): # JS shouldn't have colors usually but maybe?
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                except:
                    continue

                for i, line in enumerate(lines):
                    lower_line = line.lower()
                    
                    found = []
                    for bad in known_bads:
                        # Simple keyword check needs boundaries for words
                        if bad.startswith('#'):
                            if bad.lower() in lower_line:
                                # Ensure we don't flag our own hovers if strictly ok, 
                                # but assume anything in known_bads IS bad.
                                found.append(bad)
                        else:
                            # word check
                            if re.search(r'\b' + re.escape(bad) + r'\b', lower_line):
                                # context check: ignore "redhat", "redirect", etc if just substring
                                # regex handles \b
                                found.append(bad)
                    
                    # Also check literal #ff0000 etc
                    if '#ff0000' in lower_line: found.append('#ff0000')
                    
                    if found:
                        print(f"[{file}:{i+1}] Found {found} -> {line.strip()[:100]}")

if __name__ == "__main__":
    deep_red_audit()
