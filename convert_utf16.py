import sys

try:
    with open('p:\\AI-website-clone\\old_style.css', 'r', encoding='utf-16le') as f:
        content = f.read()
    with open('p:\\AI-website-clone\\old_style_utf8.css', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Conversion successful.")
except Exception as e:
    print(f"Error: {e}")
