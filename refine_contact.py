import re

file_path = 'p:/AI-website-clone/node_site/public/contact-us.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update First Column to col-md-6
# We match the first occurence of col-md-4 left-contact
content = content.replace('<div class="col-md-4 left-contact">', '<div class="col-md-6 left-contact">', 1)

# 2. Consolidate Emails
# Regex to match the email block
email_pattern = re.compile(r'<div class="fl-text">\s*<a href="mailto:admissions@saii\.siu\.edu\.in">.*?</div>', re.DOTALL)
new_email_block = """<div class="fl-text">
         <a href="mailto:aihealthcare.kmc@manipal.edu">aihealthcare.kmc@manipal.edu</a>
        </div>"""
content = email_pattern.sub(new_email_block, content)

# 3. Remove WhatsApp/QR Section
# Can match by the header unique to it
whatsapp_pattern = re.compile(r'\s*<div class="col-md-4 left-contact">\s*<h3>\s*Connect with Us on WhatsApp\s*</h3>.*?</div>\s*</div>', re.DOTALL)
# Actually, the closing div count is tricky in regex. 
# Let's try to match the specific content structure we saw.
# It was:
# <div class="col-md-4 left-contact">
#  <h3>
#   Connect with Us on WhatsApp
#  </h3>
#  <div class="whp">
#   <img alt="SAII – Contact Information" src="/assets/images/scan.webp"/>
#  </div>
# </div>

# We will try to replace this whole block with empty string.
# Since the class is same as the first one (before we changed it), we rely on the H3 content.
whatsapp_block_pattern = re.compile(r'<div class="col-md-[46] left-contact">\s*<h3>\s*Connect with Us on WhatsApp\s*</h3>.*?(<div class="whp">).*?</div>\s*</div>', re.DOTALL)

# Let's try a safer find/replace block since we know the exact lines from previous read.
# But python read() might have different line endings.
# We'll use a specific unique string to identify the start and look ahead.

# Simpler approach for #3:
# Find the WhatsApp header and walk back to its parent div? No.
# Use a specific known string.
old_qr_block = """<div class="col-md-4 left-contact">
       <h3>
        Connect with Us on WhatsApp
       </h3>
       <div class="whp">
        <img alt="SAII – Contact Information" src="/assets/images/scan.webp"/>
       </div>
      </div>"""
# We try to replace this block specifically. Whitespace might be an issue.
# Let's normalize match.
content = re.sub(r'<div class="col-md-4 left-contact">\s*<h3>\s*Connect with Us on WhatsApp\s*</h3>\s*<div class="whp">\s*<img[^>]+src="/assets/images/scan.webp"/>\s*</div>\s*</div>', '', content, flags=re.DOTALL)


# 4. Update Form Column to col-md-6
# It is the div wrapping <div class="frm">
# <div class="col-md-4">
#  <div class="frm">
content = content.replace('<div class="col-md-4">\n       <div class="frm">', '<div class="col-md-6">\n       <div class="frm">')
content = content.replace('<div class="col-md-4">\r\n       <div class="frm">', '<div class="col-md-6">\r\n       <div class="frm">') 
# Fallback regex
content = re.sub(r'<div class="col-md-4">\s*<div class="frm">', '<div class="col-md-6">\n       <div class="frm">', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updates applied.")
