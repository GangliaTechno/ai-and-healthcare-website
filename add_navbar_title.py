
import os
import re

def add_navbar_title():
    base_dir = r"p:\AI-website-clone\node_site\public"
    
    # Matching the logo <a> block in top-left
    # We look for <a href="index.html"> followed by the <img>
    # Since we recently updated the logo to use alt="MAHE", we can use that.
    # Pattern: <a href="index.html">\s*<img[^>]*alt="MAHE"[^>]*>\s*</a>
    
    # Note: We need to capture the optional whitespace and the img tag content to reconstruct it generally,
    # or just match the known structure we just established.
    
    pattern = re.compile(r'(<a\s+href="index\.html">)(\s*<img\s+[^>]*src="/assets/images/logo\.webp"[^>]*>\s*)(</a>)', re.IGNORECASE)
    
    replacement_str = (
        r'\1 class="navbar-brand-wrapper"\2'
        r'\n              <div class="institute-title-lockup">'
        r'\n                <span class="dept-name">Dept of AI in Healthcare</span>'
        r'\n                <span class="college-name">Kasturba Medical College, Manipal</span>'
        r'\n              </div>\n            \3'
    )
    # Explanation of replacement:
    # \1 matches start tag. We add class="navbar-brand-wrapper" to it? 
    # Wait, \1 is `<a href="index.html">`. We want to change it to `<a href="index.html" class="navbar-brand-wrapper">`.
    # Using string replacement might be safer than relying on \1 if we change attributes.
    
    # Let's do a more robust string construction in a callback function.
    
    print("--- Adding Navbar Title Lockup ---")
    
    count = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                fpath = os.path.join(root, file)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    continue
                
                # Check if already updated (avoid duplication)
                if 'institute-title-lockup' in content:
                    print(f"Skipping {file} (already updated)")
                    continue
                    
                # Search
                if pattern.search(content):
                    # We need to change the <a> tag to add the class, and insert the div before </a>
                    
                    def replacement_func(match):
                        img_tag = match.group(2).strip() # The image tag
                        
                        return (
                            '<a href="index.html" class="navbar-brand-wrapper">\n'
                            f'              {img_tag}\n'
                            '              <div class="institute-title-lockup">\n'
                            '                <span class="dept-name">Dept of AI in Healthcare</span>\n'
                            '                <span class="college-name">Kasturba Medical College, Manipal</span>\n'
                            '              </div>\n'
                            '            </a>'
                        )
                    
                    new_content = pattern.sub(replacement_func, content)
                    
                    if new_content != content:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated {file}")
                        count += 1
                else:
                    print(f"No match in {file}")

    print(f"Total files updated: {count}")

if __name__ == "__main__":
    add_navbar_title()
