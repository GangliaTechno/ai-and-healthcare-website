import re
import os

def update_fonts():
    style_css_path = 'node_site/public/assets/css/style.css'
    index_css_path = 'node_site/public/assets/css/index.css'
    
    with open(style_css_path, 'r', encoding='utf-8') as f:
        style_content = f.read()
        
    # Replace the Google Fonts import
    style_content = re.sub(
        r'@import url\([^)]*fonts\.googleapis\.com[^)]*\);',
        r"@import url('https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');",
        style_content
    )
    
    # Replace all font-family definitions in style.css
    style_content = re.sub(
        r'font-family:\s*[^;]+;',
        r"font-family: 'Ubuntu', sans-serif;",
        style_content
    )
    
    with open(style_css_path, 'w', encoding='utf-8') as f:
        f.write(style_content)
        
    with open(index_css_path, 'r', encoding='utf-8') as f:
        index_content = f.read()
        
    # Replace all font-family definitions in index.css
    index_content = re.sub(
        r'font-family:\s*[^;]+;',
        r"font-family: 'Ubuntu', sans-serif;",
        index_content
    )
    
    with open(index_css_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

if __name__ == '__main__':
    update_fonts()
    print("Fonts updated to Ubuntu.")
