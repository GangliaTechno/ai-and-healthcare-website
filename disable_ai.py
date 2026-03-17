import os
import re

directory = 'p:/AI-website-clone/node_site/public/'

# Improved pattern:
# The script has unique content "bot-frame.geta.ai/output.js".
# We want to match the surrounding <script>...</script> block.
# We will match: <script> followed by any content that includes that URL, followed by </script>.
# Minimal matching for <script> to ensure we don't start from an earlier script.

# Regex:
# <script>\s*\(function.*?bot-frame\.geta\.ai/output\.js.*?</script>
# Using DOTALL to match across newlines.

pattern = re.compile(
    r'(<script>\s*[^<]*?bot-frame\.geta\.ai/output\.js.*?</script>)', 
    re.DOTALL | re.IGNORECASE
)

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
        
        # Check if already commented
        # If the block is "<!-- <script> ... </script> -->", we want to avoid matching the inner part.
        # But regex finds the first <script>.
        # We can detect if the MATCH includes "<!--" before it? No.
        
        # Let's iterate over matches and decide.
        def replace_callback(match):
            full_match = match.group(0)
            # Check context in original content?
            # Easier: Just replace it.
            # BUT, if we run this on: "<!-- <script>...</script> -->"
            # The regex will match "<script>...</script>" inside.
            # Then we wrap it: "<!-- <!-- <script>...</script> --> -->" which is bad HTML.
            
            # Simple heuristic:
            # If the char immediately before the match is '-' check further.
            start = match.start()
            if start >= 4 and content[start-4:start] == '<!--':
                return full_match # Already commented
            if start >= 5 and content[start-5:start].strip().endswith('<!--'):
                 return full_match
            
            return f'<!-- {full_match} -->'

        # We can't easily use callback with context in Python re.sub effectively for "outside" checks without capturing surrounding.
        # Let's verify manually.
        
        # New approach: Capture potential comment start before?
        # r'(<!--\s*)?(<script>.*?geta.*?script>)'
        
        pattern_check = re.compile(
            r'(<!--\s*)?(<script>\s*[^<]*?bot-frame\.geta\.ai/output\.js.*?</script>)',
            re.DOTALL | re.IGNORECASE
        )
        
        def sub_func(match):
            comment_prefix = match.group(1)
            original_script = match.group(2)
            
            if comment_prefix:
                # It is already commented
                return match.group(0)
            
            return f'<!-- {original_script} -->'
            
        new_content = pattern_check.sub(sub_func, content)

        if new_content != original_content:
            with open(filepath, 'w', encoding=enc) as f:
                f.write(new_content)
            print(f"Disabled AI in {filename}")
            count += 1
        else:
            # print(f"No active AI script found in {filename}")
            pass

print(f"Disabled AI Assistant in {count} files.")
