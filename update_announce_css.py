import sys

# Append new styles to index.css
css_path = r"p:\AI-website-clone\node_site\public\assets\css\index.css"

new_styles = """
/* MAHE Announcement Bar Typography Update */
.announcebar-wp {
  font-family: 'Montserrat', sans-serif !important;
}

.announcebar-wp .announce-txt {
  font-family: 'Montserrat', sans-serif !important;
  font-weight: 700 !important;
  letter-spacing: 0.5px !important;
  text-transform: uppercase !important;
}

.announcebar-wp .js-announce-carousel a {
  font-family: 'Montserrat', sans-serif !important;
  font-weight: 500 !important;
  font-size: 14px !important;
  letter-spacing: 0.2px !important;
}
"""

with open(css_path, "a", encoding="utf-8") as f:
    f.write(new_styles)

print("CSS updated successfully.")
