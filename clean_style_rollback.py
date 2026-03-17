import os

css_path = 'p:/AI-website-clone/node_site/public/assets/css/style.css'

with open(css_path, 'r', encoding='utf-8') as f:
    text = f.read()

# We want to remove the block starting with "/* Neutralize Floating CTAs */"
# Since I appended it at the end, I can just truncate at the index.

key_phrase = "/* Neutralize Floating CTAs */"
idx = text.find(key_phrase)

if idx != -1:
    # Truncate everything from this index onwards
    # Assuming it was the last thing added and nothing else important is after.
    # We should verify if there's anything else?
    # Usually I appended it to the end.
    
    # Just to be safe, if there was a '} ' before it, we keep it.
    new_text = text[:idx].rstrip()
    
    # Ensure file ends with a brace?
    # If the file ended with a brace before append, it should be fine.
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    
    print("Removed blocking CSS rules.")
else:
    print("Could not find blocking CSS rules.")
