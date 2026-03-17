
import os
import re

def check_inline_styles():
    base_dir = r"p:\AI-website-clone\node_site\public"
    color_pat = re.compile(r'style="[^"]*(color|background|border)[^"]*:[^"]*(#|rgb|red|blue|maroon)[^"]*"', re.IGNORECASE)
    
    print("--- Inline Style Check ---")
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if not file.endswith('.html'): continue
            
            fpath = os.path.join(root, file)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for m in color_pat.finditer(content):
                # Filter out our known good colors or common benign ones if necessary, but manual review is best
                match_str = m.group(0)
                if '#E85626' in match_str or '#e85626' in match_str: continue # accepted
                if '#fff' in match_str or '#000' in match_str: continue # accepted
                
                print(f"Found inline color in {file}: {match_str}")

if __name__ == "__main__":
    check_inline_styles()
