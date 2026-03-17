import os
import re

directory = r"p:\AI-website-clone\node_site\public"

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        
        # Determine encoding by trying utf-8 and falling back to utf-16
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            encoding_used = 'utf-8'
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='utf-16') as f:
                content = f.read()
            encoding_used = 'utf-16'
        
        # Replace <title>...</title> safely
        new_content = re.sub(r'<title>.*?</title>', '<title>Dept of AI in Healthcare</title>', content, flags=re.DOTALL|re.IGNORECASE)
        
        if content != new_content:
            with open(filepath, 'w', encoding=encoding_used) as f:
                f.write(new_content)
            print(f"Updated {filename}")
