
import os
import re

css_dir = r"p:\AI-website-clone\node_site\public\assets\css"
files = [f for f in os.listdir(css_dir) if f.endswith(".css")]

regex = re.compile(r"\.btn-for-mobile\s*\{([^}]*)\}", re.DOTALL)
regex_display_none = re.compile(r"display\s*:\s*none")

for file in files:
    path = os.path.join(css_dir, file)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple search for the class name
    if ".btn-for-mobile" in content:
        print(f"--- Matches in {file} ---")
        # Print lines matching class
        lines = content.split('\n')
        for i, line in enumerate(lines):
             if ".btn-for-mobile" in line:
                 print(f"Line {i+1}: {line.strip()}")
                 # If it looks like a rule start, print next few lines
                 if "{" in line:
                     for j in range(1, 10):
                         if i+j < len(lines):
                             subline = lines[i+j].strip()
                             print(f"  {subline}")
                             if "}" in subline:
                                 break
        print("\n")
