import requests
from bs4 import BeautifulSoup
import re

url = "https://www.manipal.edu/mu.html"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try to find announcement bar
    # it might have classes like 'announcement', 'alert', 'notice', 'marquee'
    announcements = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') and any('announce' in c.lower() or 'alert' in c.lower() or 'marquee' in c.lower() or 'notice' in c.lower() for c in tag.get('class')))
    
    for idx, a in enumerate(announcements):
        print(f"Announcement Element {idx}:")
        print(a.prettify()[:500])
        print("Classes:", a.get('class'))
        print("-" * 40)
        
    print("CSS Links:")
    for link in soup.find_all('link', rel='stylesheet'):
        print(link.get('href'))
else:
    print(f"Failed to fetch {url}, status code: {response.status_code}")
