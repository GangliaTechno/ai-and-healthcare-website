import os
import re

css_path = 'p:/AI-website-clone/node_site/public/assets/css/style.css'

with open(css_path, 'rb') as f:
    content = f.read()

# The corrupted part likely starts near the end.
# We look for the "/* Neutralize Floating CTAs */" pattern but in wide chars or just scrambled.
# It seems the `type` command output UTF-16 LE BOM or similar.
# Let's try to locate the end brace "}" of the previous block and cut off everything after, then append the Clean CSS.

# The last valid CSS was likely the media query closing brace.
# We can search for the last "}" before the corruption start.
# Or we can just try to decode and filter.

try:
    decoded = content.decode('utf-8')
    # If it decodes fine, maybe the spaces are literal spaces?
    # " / *   N e u t r a l i z e ..."
    # If so, we can just replace it.
    
    # Let's try to find the "/* Neutralize" block essentially.
    
    # We want to replace the whole block:
    # /* Neutralize Floating CTAs */ ... }
    # with
    # /* Neutralize Floating CTAs */
    # .call-link, .wht { ... }
    
    # But first, let's clean the wide chars if they are just spaces 0x00 ??
    # If `content` is binary, we can check.
    pass
except:
    pass

# Simplified approach:
# Find the end of validity.
# The `type` command on Windows PowerShell might produce UTF-16LE.
# 0x0d 0x00 0x0a 0x00 ...
# Let's look for the byte sequence of "/* Neutralize" in ASCII vs UTF-16

marker = b'/* Neutralize Floating CTAs */'
# It might appear as wide char in the file:
# b'/\x00*\x00 \x00N\x00...'

# Let's just strip everything after the last known good closure '}' and append valid utf-8.
# The corrupted output showed "}/ * N e u t r a l i z e..."
# So there is a "}" right before it.

# Let's find the last occurrence of "}" that IS NOT followed by wide chars immediately?
# Actually, simply reading the file as utf-8 (ignoring errors) and stripping the end might work.

# Let's try to read as binary, find the "/* Neutralize" (or its broken version), and truncate.
# The broken version seems to have spaces between every char.

# Strategy:
# 1. Read binary.
# 2. Look for where the corruption starts.
#    The corruption starts after the last valid "}".
#    The corruption generally looks like valid text interleaved with nulls or spaces.
#    We will just truncate at the last '}' that is followed by the bad block.

# The bad block text: "/ *   N e u t r a l i z e"
# In ASCII: 2f 20 2a 20 20 20 4e ...
# Wait, the `view_file` showed spaces, not nulls. " / * "
# This implies it might have been CP1252 or similar interpretation of UTF-16.

# Let's use a robust replacement.
# We will regenerate the end of the file.

# We will read as text (utf-8 or latin1), finding the point where "Neutralize Floating CTAs" starts (in any form) and cut there.

# Robust fix:
# 1. Read file.
# 2. Identify where our previous append started. It starts with ".call-link" or ".wht" or "/* Neutralize".
# 3. Cut off everything from there.

with open(css_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# We look for the start of the "Neutralize" block.
# Since the text might be corrupted with spaces, we regex for it.

pattern = re.compile(r'/\*\s*N\s*e\s*u\s*t\s*r\s*a\s*l\s*i\s*z\s*e', re.IGNORECASE)
match = pattern.search(text)

cutoff_index = -1

if match:
    cutoff_index = match.start()
else:
    # Try looking for .call-link ... display: none
    pattern2 = re.compile(r'\.call-link.*display:\s*none', re.DOTALL)
    match2 = pattern2.search(text)
    if match2:
        cutoff_index = match2.start()
        # Ensure we go back to the comment if possible, but finding the previous } is safer.
        last_brace = text.rfind('}', 0, cutoff_index)
        if last_brace != -1:
             cutoff_index = last_brace + 1

if cutoff_index != -1:
    clean_text = text[:cutoff_index]
else:
    # If we couldn't find the bad block, maybe it's cleaner than we thought? 
    # Or maybe we are blind.
    # Let's assume valid CSS ends at the last "}" before the end of file?
    # No, that might catch the corrupted one.
    
    # Let's just assume the file is mostly good and we just need to append the NEW rule 
    # and overwrite the BAD rule if we can find it. 
    # But replacing is better.
    
    # As a fallback, if we can't find the bad block, we verify if the bad block is actually there?
    # Get-Content showed it IS there.
    
    # Let's just truncate at the last '}' that is NOT part of the bad block.
    # The bad block has ".wht" and ".video-hub".
    # Find the index of ".video-hub".
    idx = text.find('.video-hub')
    if idx != -1:
        # Go back to the } before this.
        last_brace = text.rfind('}', 0, idx)
        clean_text = text[:last_brace+1]
    else:
        # If .video-hub isn't there, maybe we already fixed it or encoding masked it?
        # Check for apply-steps-btn
        idx2 = text.find('.apply-steps-btn')
        if idx2 != -1:
             last_brace = text.rfind('}', 0, idx2)
             clean_text = text[:last_brace+1]
        else:
             # Just keep whole text
             clean_text = text

# Now append the correct CSS (without video-hub/apply-steps-btn)
new_css = """
/* Neutralize Floating CTAs */
.call-link, 
.wht {
    display: none !important;
    pointer-events: none !important;
    width: 0 !important;
    height: 0 !important;
    position: static !important;
}
"""

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(clean_text.strip() + new_css)

print("Fixed style.css via truncation and append.")
    
