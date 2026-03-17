
import os

def append_css():
    css_file = r"p:\AI-website-clone\node_site\public\assets\css\style.css"
    new_styles_file = "navbar_layout_fix.css"
    
    if not os.path.exists(new_styles_file):
        print(f"Error: {new_styles_file} not found.")
        return

    try:
        with open(new_styles_file, 'r', encoding='utf-8') as f:
            new_css = f.read()
            
        with open(css_file, 'a', encoding='utf-8') as f:
            f.write("\n" + new_css)
            
        print(f"Successfully appended styles to {css_file}")
    except Exception as e:
        print(f"Error appending CSS: {e}")

if __name__ == "__main__":
    append_css()
