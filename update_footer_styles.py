import os
import re

directory = r"p:\AI-website-clone\node_site\public"

# The specific span block that we need to update
search_pattern = r'<span style="display:\s*block;\s*font-weight:\s*400;\s*color:\s*#555;\s*font-size:\s*14px;\s*line-height:\s*1\.4;">(.*?)</span>'
replacement_string = r'<span class="college-name">\1</span>'

# Second pattern for the other span style
search_pattern_dept = r'<span style="display:\s*block;\s*font-weight:\s*700;\s*color:\s*#000;\s*font-size:\s*16px;\s*line-height:\s*1\.2;">(.*?)</span>'
replacement_string_dept = r'<span class="dept-name">\1</span>'


for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            encoding_used = 'utf-8'
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='utf-16') as f:
                content = f.read()
            encoding_used = 'utf-16'
        
        # Replace the hardcoded spans to use the class names we styled in CSS instead
        new_content = re.sub(search_pattern, replacement_string, content, count=0)
        new_content = re.sub(search_pattern_dept, replacement_string_dept, new_content, count=0)
        
        if content != new_content:
            with open(filepath, 'w', encoding=encoding_used) as f:
                f.write(new_content)
            print(f"Updated classes in {filename}")
