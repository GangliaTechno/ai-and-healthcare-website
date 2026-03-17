
import os
import re

def update_logos():
    base_dir = r"p:\AI-website-clone\node_site\public"
    
    # 1. Navbar Logo Regex
    # Matches <img ... src="...logo.png" ... > inside <a> or top-left
    # Just looking for the specific logo.png tag is usually safe enough if specific attributes match style.
    # Current: <img alt="Logo of Symbiosis..." src="/assets/images/logo.png" />
    # New: <img alt="MAHE" src="/assets/images/logo.webp" />
    
    navbar_logo_search = re.compile(r'<img[^>]*src=["\']/assets/images/logo\.png["\'][^>]*>', re.IGNORECASE)
    navbar_logo_replace = '<img alt="MAHE" src="/assets/images/logo.webp" />'
    
    # 2. Footer Logo Regex
    # Matches the specific ft-logo div content we just built or the old title
    # We normalized the footer recently, so it looks like:
    # <div class="ft-logo">\s*<h3 ...>...</h3>\s*</div>  (or the <img> tag if user edited some)
    # Let's target the inner content of .ft-logo
    
    footer_logo_search = re.compile(r'(<div class="ft-logo">\s*)([\s\S]*?)(\s*</div>)', re.IGNORECASE)
    
    # New footer content with inline styles (replacing Tailwind)
    footer_logo_content = '<img src="/assets/images/logo.webp" alt="MAHE" style="max-width: 220px; height: auto;" />'
    
    print("--- Updating Logos ---")
    
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
                
                new_content = content
                
                # Update Navbar
                if 'logo.png' in new_content:
                    new_content = re.sub(navbar_logo_search, navbar_logo_replace, new_content)
                
                # Update Footer
                # We want to replace whatever is inside <div class="ft-logo"> with our new image
                # Be careful not to replace it if it's already done correctly.
                # Let's check if it already has logo.webp in ft-logo
                
                def footer_sub(match):
                    wrapper_start = match.group(1)
                    inner = match.group(2)
                    wrapper_end = match.group(3)
                    
                    if 'logo.webp' in inner and 'max-width' in inner:
                        return match.group(0) # Already good
                    
                    return f'{wrapper_start}\n            {footer_logo_content}\n          {wrapper_end}'

                new_content = re.sub(footer_logo_search, footer_sub, new_content)
                
                # Also fix the specific Tailwind class if user already pasted it in index.html or others
                # class="max-w-[220px] h-auto" -> style="max-width: 220px; height: auto;"
                # Regex for the img tag with that class
                tailwind_img_search = re.compile(r'<img[^>]*class="max-w-\[220px\] h-auto"[^>]*>', re.IGNORECASE)
                
                def tailwind_fix(match):
                    # extract src and alt if possible, or just replace the tag if we know it's the logo
                    m_str = match.group(0)
                    if 'logo.webp' in m_str:
                         return '<img src="/assets/images/logo.webp" alt="MAHE" style="max-width: 220px; height: auto;" />'
                    return m_str

                new_content = re.sub(tailwind_img_search, tailwind_fix, new_content)


                if new_content != content:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {file}")
                    count += 1
    
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    update_logos()
