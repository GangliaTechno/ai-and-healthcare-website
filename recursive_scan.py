
import os
import re

def scan_all_files():
    base_dir = r"p:\AI-website-clone\node_site\public"
    
    # regex for gradients
    gradient_pat = re.compile(r'(linear|radial)-gradient\s*\((.*?)\)', re.IGNORECASE | re.DOTALL)
    
    # regex for potential red colors
    red_hex = re.compile(r'#(?:(?:[c-fC-F][0-9a-fA-F]{2})|(?:[c-fC-F][0-9a-fA-F]{5}))\b') # Rough check for starts with C-F (reddish?) - actually high R is first two chars.
    # Better red check: #RRGGBB where RR > AA and GB < 88? 
    # Let's just look for keyword 'red' or specific high hexes or known bad hexes.
    known_bad_hex = ['#9e181d', '#bf2617', '#b01116', '#af251c', '#c2272c', '#ff4d4d', '#c4161c', '#b20000']
    
    print("--- Recursive Scan for Red Gradients ---")
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if not file.endswith(('.html', '.css')):
                continue
                
            fpath = os.path.join(root, file)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                continue

            # Check for gradients
            for m in gradient_pat.finditer(content):
                g_content = m.group(0)
                # Check if this gradient contains red signals
                is_suspicious = False
                
                # Check known bad hexes
                for bad in known_bad_hex:
                    if bad.lower() in g_content.lower():
                        is_suspicious = True
                        print(f"FOUND BAD HEX in GRADIENT: {bad} in {os.path.basename(fpath)}")
                
                # Check specifically for 'red', 'crimson', 'maroon', etc
                if re.search(r'\b(red|crimson|maroon|firebrick)\b', g_content, re.IGNORECASE):
                     is_suspicious = True
                     print(f"FOUND RED KEYWORD in GRADIENT: {os.path.basename(fpath)} -> {g_content[:50]}...")

                # Check for rgb(high, low, low)
                # This is harder with regex, but let's try strict rgb(R, G, B) parsing if needed.
                # For now let's just print all gradients to be safe if they aren't obviously white/black
                if not is_suspicious:
                     # Filter out benign ones
                     lower_g = g_content.lower()
                     if ('#fff' in lower_g or '#000' in lower_g or 'transparent' in lower_g) and not ('#e85626' in lower_g):
                         # likely safe black/white
                         pass
                     elif '#e85626' in lower_g:
                         # safe, it's our theme color
                         pass
                     else:
                         print(f"CHECK GRADIENT in {os.path.basename(fpath)}: {g_content[:100]}...")

            # Check for specific classes mentioned by user
            user_classes = ['.apply-now', '.apply-btn', '.cta', '.highlight']
            for uc in user_classes:
                if uc in content:
                    print(f"FOUND CLASS {uc} in {os.path.basename(fpath)}")

if __name__ == "__main__":
    scan_all_files()
