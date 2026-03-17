
import re

filepath = r"p:\AI-website-clone\node_site\public\assets\css\style.css"
search_terms = ["apply-now-btn", "btn-for-mobile", "btn-1", "btn-2", ".read-more a"]

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("--- CSS Matches ---")
# Simple regex to find selectors and their blocks (rough approximation)
# finding lines with the terms
lines = content.split('\n')
for i, line in enumerate(lines):
    for term in search_terms:
        if term in line:
            # print context
            start = max(0, i-2)
            end = min(len(lines), i+5)
            print(f"Line {i+1}: {line.strip()}")
            # print(f"Context:\n" + "\n".join(lines[start:end]))
            # print("-" * 20)
