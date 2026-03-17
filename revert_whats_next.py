import os
import re

directory = 'p:/AI-website-clone/node_site/public/'

# We want to re-comment ONLY the "What's Next" buttons we just restored.
# They look like: <a class="apply-steps-btn video-hub" ...> ... </a>
# We want to wrap them in <!-- ... -->

patterns = [
    (r'(<a [^>]*class="[^"]*apply-steps-btn[^"]*".*?>.*?</a>)', r'<!-- \1 -->'),
    (r'(<a [^>]*class="[^"]*video-hub[^"]*".*?>.*?</a>)', r'<!-- \1 -->'),
]

count = 0

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        
        # Encoding handling
        content = None
        encodings = ['utf-8', 'cp1252', 'latin1']
        for enc in encodings:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None: continue

        original_content = content
        
        for pattern, replacement in patterns:
            # Check if *already* commented?
            # Regex is tricky. But if I just restored them, they shouldn't be commented.
            # But wait, if allow re-run, I should avoid double comment.
            # simpler check: if the match is surrounded by <!-- and --> ignore?
            # Or just run it. The user just asked to revert.
            
            # Simple approach: Check if it's already commented inline is hard with regex sub.
            # But since I know the state is "Clean/Restored", I can just comment.
            # BUT, to be safe, let's verify we aren't matching inside a comment?
            # Too complex for quick script. Assuming clean state from previous "Restore" step.
            
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        if content != original_content:
            with open(filepath, 'w', encoding=enc) as f:
                f.write(content)
            print(f"Re-disabled in {filename}")
            count += 1

print(f"Re-disabled 'What's Next' buttons in {count} files.")
