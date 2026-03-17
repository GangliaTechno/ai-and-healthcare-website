import os
import re

directory = 'p:/AI-website-clone/node_site/public/'

# Regex patterns to RESTORE (uncomment)
# We look for the commented blocks we created.
# They are wrapped in <!-- ... -->
# We capture the inner content.

patterns = [
    # 1. Call Link
    (r'<!--\s*(<a class="call-link".*?>.*?</a>)\s*-->', r'\1'),
    
    # 2. WhatsApp
    (r'<!--\s*(<div class="wht">.*?</div>)\s*-->', r'\1'),
    
    # 3. Floating Video/Help/steps button (What's Next)
    (r'<!--\s*(<a [^>]*class="[^"]*apply-steps-btn[^"]*".*?>.*?</a>)\s*-->', r'\1'),
    (r'<!--\s*(<a [^>]*class="[^"]*video-hub[^"]*".*?>.*?</a>)\s*-->', r'\1'),
    
    # 4. Floating Logo / Video Btn
    (r'<!--\s*(<div class="video-btn".*?>.*?</div>)\s*-->', r'\1'),
    
    # 5. IMG Overlay Custom triggers
    (r'<!--\s*(<button [^>]*class="[^"]*stepsFloatingBtn[^"]*".*?>.*?</button>)\s*-->', r'\1'),
    (r'<!--\s*(<div [^>]*class="[^"]*stepsFloatingBtn[^"]*".*?>.*?</div>)\s*-->', r'\1'),
    (r'<!--\s*(<a [^>]*id="stepsFloatingBtn"[^>]*>.*?</a>)\s*-->', r'\1')
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
            # We use re.DOTALL to match newlines inside the comment
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        if content != original_content:
            with open(filepath, 'w', encoding=enc) as f:
                f.write(content)
            print(f"Restored CTAs in {filename}")
            count += 1

print(f"Rollback complete. Restored CTAs in {count} files.")
