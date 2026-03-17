import requests
from bs4 import BeautifulSoup
import re

url = "https://www.manipal.edu/mu.html"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try to find announcement bar
    announcements = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') and any('announce' in c.lower() or 'alert' in c.lower() or 'marquee' in c.lower() or 'notice' in c.lower() for c in tag.get('class')))
    
    css_links = []
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href:
            if href.startswith('/'):
                href = f"https://www.manipal.edu{href}"
            css_links.append(href)
            
    print(f"Found {len(css_links)} CSS links.")
    
    # Let's download the first few CSS files and search for 'announce' to see the font-family
    for css_url in css_links:
        try:
            css_resp = requests.get(css_url, headers=headers)
            if css_resp.status_code == 200:
                css_text = css_resp.text
                if 'announce' in css_text.lower():
                    print(f"\nCSS file with 'announce': {css_url}")
                    # Extract rules containing 'announce'
                    blocks = re.findall(r'(\.[^{]*announce[^{]*\{[^}]*\})', css_text, re.IGNORECASE)
                    for b in blocks:
                        print(b)
        except Exception as e:
            pass

else:
    print("Failed")
