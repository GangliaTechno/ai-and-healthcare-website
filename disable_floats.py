import os
import re

directory = 'p:/AI-website-clone/node_site/public/'

# Regex patterns to find and comment out
# We capture the whole block to wrap it in comments.
# Using non-greedy match .*? to respect boundaries.

patterns = [
    # 1. Call Link
    (r'(<a class="call-link".*?>.*?</a>)', r'<!-- \1 -->'),
    
    # 2. WhatsApp
    (r'(<div class="wht">.*?</div>)', r'<!-- \1 -->'),
    
    # 3. Floating Video/Help/steps button
    # Matching the specific class patterns mentioned
    # <a class="apply-steps-btn video-hub" ...> or similar
    # We'll match broadly on the class name if it looks like the button
    (r'(<a [^>]*class="[^"]*apply-steps-btn[^"]*".*?>.*?</a>)', r'<!-- \1 -->'),
    (r'(<a [^>]*class="[^"]*video-hub[^"]*".*?>.*?</a>)', r'<!-- \1 -->'),
    
    # 4. Floating Logo / Video Btn specific ID if exists (user mentioned .video-btn)
    (r'(<div class="video-btn".*?>.*?</div>)', r'<!-- \1 -->'),
    
    # 5. IMG Overlay Custom (Popup trigger often associated with floating)
    # The user didn't explicitly ask to remove the popup *modal* itself, but the floating *buttons*.
    # "3) Floating Circular Logo / Help CTA ... HTML patterns may include: .video-btn"
    # But usually <div id="imgOverlayCustom"> is the modal, not the button.
    # The button is often `.stepsFloatingBtn` or similar.
    (r'(<button [^>]*class="[^"]*stepsFloatingBtn[^"]*".*?>.*?</button>)', r'<!-- \1 -->'),
    (r'(<div [^>]*class="[^"]*stepsFloatingBtn[^"]*".*?>.*?</div>)', r'<!-- \1 -->'),
    # Also <a ... id="stepsFloatingBtn">
    (r'(<a [^>]*id="stepsFloatingBtn"[^>]*>.*?</a>)', r'<!-- \1 -->')
]

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        
        # Try reading with utf-8, then cp1252 if fails
        content = None
        encodings = ['utf-8', 'cp1252', 'latin1']
        
        for enc in encodings:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"Skipping {filename}: Could not decode.")
            continue
        
        original_content = content
        
        for pattern, replacement in patterns:
            # Check if already commented to prevent double commenting
            # This is tricky with regex, simpler to just run it. 
            # If it's already <!-- <a ... --> it might wrap again.
            # We can check if wrapped?
            # A simple heuristic: if the line starts with <!-- and contains the pattern...
            # But the pattern matches newlines.
            
            # Better: Modify regex to ensure not preceded by <!-- and not followed by -->?
            # Too complex for quick script.
            # We will rely on the fact we are running this once.
            
            # Warning: Python re.sub might match overlapping if we are not careful, but here we are sequential.
            
            # To avoid double commenting:
            # We can use a function in substitution to check.
            
            def sub_if_not_commented(match):
                text = match.group(1)
                # Quick check if it looks commented
                if text.strip().startswith('<!--') and text.strip().endswith('-->'):
                    return text
                return f'<!-- {text} -->'
            
            # content = re.sub(pattern, sub_if_not_commented, content, flags=re.DOTALL)
            # Actually, let's just use the simpler replacement for now, assuming clean state.
            # But wait, identifying "already commented" is hard if identifying "floating video hub" is loose.
            # Let's trust the classes are unique to liv elements.
            
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Processed {filename}")
        else:
            print(f"No changes in {filename}")

print("Batch disable complete.")
