
import os

def update_copyright():
    base_dir = r"p:\AI-website-clone\node_site\public"
    
    # Target text as seen in index.html (trimmed)
    target_text_1 = "© Copyright SAII. All Rights Reserved"
    target_text_2 = "&copy; Copyright SAII. All Rights Reserved" # just in case
    
    replacement_text = "© 2026 Manipal Academy of Higher Education"
    
    print("--- Updating Copyright Text ---")
    
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
                if target_text_1 in new_content:
                    new_content = new_content.replace(target_text_1, replacement_text)
                
                if target_text_2 in new_content:
                    new_content = new_content.replace(target_text_2, replacement_text)
                
                if new_content != content:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {file}")
                    count += 1
    
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    update_copyright()
