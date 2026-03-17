
import os

def batch_fix_reds():
    base_dir = r"p:\AI-website-clone\node_site\public"
    
    # Replacement rules
    # Target specific bad hexes found in audit
    replacements = {
        '#AF251C': '#E85626',
        '#af251c': '#E85626',
        '#C2272C': '#E85626',
        '#c2272c': '#E85626',
        '#b20000': '#d1491e' # Dark red -> Dark orange for gradients if needed, or just theme orange? 
                              # User said "Replace it with MAHE Orange (#E85626)... OR replace it with neutral gray"
                              # But for gradients/shadows, a darker orange is better. 
                              # Let's stick to the mapping I used in CSS: #d1491e.
                              # Wait, the audit found #c2272c and #af251c mostly.
    }
    
    print("--- Batch Fixing Reds ---")
    
    count = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            # Process HTML and SVGs
            if file.endswith(('.html', '.svg')):
                fpath = os.path.join(root, file)
                
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    continue
                
                new_content = content
                modified = False
                
                for bad, good in replacements.items():
                    if bad in new_content:
                        new_content = new_content.replace(bad, good)
                        modified = True
                
                # Special handling for 'red' keyword in style attributes or SVGs if unambiguous?
                # The audit showed: [contact-us.html:284] class="... text-red"
                # I'll handle .text-red in CSS, but the class name itself in HTML doesn't need changing 
                # if I change the CSS definition.
                # However, if I want to be clean, I could rename the class, but "Modify existing classes only" was the rule.
                # So changing the CSS definition of .text-red is better than changing HTML class names.
                
                if modified:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed {file}")
                    count += 1

    print(f"Total files updated: {count}")

if __name__ == "__main__":
    batch_fix_reds()
