
import os
import re

directory = r"p:\AI-website-clone\node_site\public"
viewport_tag = '<meta content="width=device-width, initial-scale=1,user-scalable=0" name="viewport" />'
responsive_css_link = '<link href="/assets/css/responsive.css" rel="stylesheet" />'

def update_file(filepath):
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'windows-1252']
    content = None
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        print(f"Failed to read {os.path.basename(filepath)}")
        return

    changed = False
    
    # Ensure viewport tag exists and is correct
    if viewport_tag not in content:
        if '<meta name="viewport"' in content or '<meta content="width=device-width' in content:
            # Replace existing different viewport tag
            content = re.sub(r'<meta [^>]*name="viewport"[^>]*>', viewport_tag, content)
            changed = True
        else:
            # Insert after charset or x-ua-compatible
            head_match = re.search(r'<head>', content, re.IGNORECASE)
            if head_match:
                insert_pos = head_match.end()
                # Try to insert after other metas
                last_meta = list(re.finditer(r'<meta [^>]*>', content, re.IGNORECASE))
                if last_meta:
                    for m in reversed(last_meta):
                        if m.start() < 1000:
                            insert_pos = m.end()
                            break
                content = content[:insert_pos] + "\n  " + viewport_tag + content[insert_pos:]
                changed = True

    # Ensure responsive.css is linked
    if 'assets/css/responsive.css' not in content:
        style_match = re.search(r'<link [^>]*style\.css[^>]*>', content)
        if style_match:
            insert_pos = style_match.end()
            content = content[:insert_pos] + "\n  " + responsive_css_link + content[insert_pos:]
            changed = True

    if changed:
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        update_file(os.path.join(directory, filename))
