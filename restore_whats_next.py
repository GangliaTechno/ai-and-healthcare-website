import os
import re

directory = 'p:/AI-website-clone/node_site/public/'

# Pattern to find the specific commented out "What's Next" buttons
# They look like: <!-- <a class="apply-steps-btn video-hub" ...> ... </a> -->
# We need to be careful to match exactly the ones we commented out.
# My disable script used: `<!-- \1 -->` wrapping the whole tag.

# Pattern: match `<!-- ` followed by `<a` containing `apply-steps-btn` or `video-hub` followed by `-->`
# We need to capture the inner content to restore it.
pattern = re.compile(r'<!--\s*(<a [^>]*class="[^"]*(?:apply-steps-btn|video-hub)[^"]*"[^>]*>.*?</a>)\s*-->', re.DOTALL)

count = 0

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        
        # Encoding handling as before
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
        
        # Substitute: restore the captured group
        new_content = pattern.sub(r'\1', content)
        
        if new_content != original_content:
            with open(filepath, 'w', encoding=enc) as f:
                f.write(new_content)
            print(f"Restored in {filename}")
            count += 1

print(f"Restored 'What's Next' buttons in {count} files.")
