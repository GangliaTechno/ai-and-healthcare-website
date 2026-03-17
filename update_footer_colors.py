
import os
import glob

def update_footer_color():
    base_dir = r"p:\AI-website-clone\node_site\public"
    files = glob.glob(os.path.join(base_dir, "*.html"))
    
    target_str = 'style="color:#AF251C"'
    replacement_str = 'style="color:#E85626"'
    
    count = 0
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if target_str in content:
            new_content = content.replace(target_str, replacement_str)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(fpath)}")
            count += 1
            
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    update_footer_color()
