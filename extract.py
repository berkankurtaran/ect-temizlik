import ssl
import urllib.request
import re
from collections import Counter
from urllib.parse import urljoin

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://yesildonusum.sanayi.gov.tr/"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
    css_links = re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"', html)
    
    colors = []
    for link in css_links:
        full_url = urljoin(url, link)
        try:
            req_css = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
            css = urllib.request.urlopen(req_css, context=ctx).read().decode('utf-8', errors='ignore')
            hex_colors = re.findall(r'#[0-9a-fA-F]{3,6}', css)
            colors.extend([c.lower() for c in hex_colors])
        except Exception as e:
            pass
            
    counter = Counter(colors)
    for c, count in counter.most_common(15):
        print(f"{c}: {count}")
except Exception as e:
    print("Error:", e)
