
import re
import os

def analyze_colors():
    files = [
        r"p:\AI-website-clone\node_site\public\assets\css\style.css",
        r"p:\AI-website-clone\node_site\public\assets\css\index.css",
        r"p:\AI-website-clone\node_site\public\assets\css\responsive.css"
    ]

    # Regex patterns
    hex_pat = re.compile(r'#(?:[0-9a-fA-F]{3}){1,2}')
    rgb_pat = re.compile(r'rgba?\([^)]*\)')
    named_pat = re.compile(r'\b(red|blue|green|pink|purple|cyan|magenta|yellow|orange|brown|maroon|navy|teal|olive|lime|crimson|darkred|darkblue|skyblue|royalblue|firebrick)\b', re.IGNORECASE)

    for file_path in files:
        if not os.path.exists(file_path):
            continue
            
        print(f"--- Analyzing {os.path.basename(file_path)} ---")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
             with open(file_path, 'r', encoding='latin-1') as f:
                lines = f.readlines()

        for i, line in enumerate(lines):
            # Hex
            hex_matches = hex_pat.findall(line)
            for m in hex_matches:
                # Filter out likely neutrals or already converted
                if m.lower() not in ['#fff', '#ffffff', '#000', '#000000', '#f8f9fa', '#e85626', '#cccccc', '#ccc']:
                    print(f"Line {i+1} [HEX]: {m} -> {line.strip()}")

            # RGB
            rgb_matches = rgb_pat.findall(line)
            for m in rgb_matches:
                 if '0, 0, 0' not in m and '255, 255, 255' not in m: # Ignore simple black/white alphas
                    print(f"Line {i+1} [RGB]: {m} -> {line.strip()}")
            
            # Named
            named_matches = named_pat.findall(line)
            for m in named_matches:
                print(f"Line {i+1} [NAMED]: {m} -> {line.strip()}")

if __name__ == "__main__":
    analyze_colors()
