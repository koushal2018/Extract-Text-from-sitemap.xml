import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def extract_urls_from_sitemap(sitemap_path):
    with open(sitemap_path, 'r') as file:
        tree = ET.parse(file)
    root = tree.getroot()
    
    urls = []
    for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        if loc is not None:
            urls.append(loc.text)
    return urls

def fetch_content_from_urls(urls):
    contents = {}
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            contents[url] = soup.text
        else:
            contents[url] = f"Error {response.status_code}"
    return contents

sitemap_path = 'path/to/sitemap.xml'
urls = extract_urls_from_sitemap(sitemap_path)
contents = fetch_content_from_urls(urls)

def save_contents_to_file(contents, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for url, content in contents.items():
            file.write(f"URL: {url}\n")
            file.write(f"Content:\n{content}\n")
            file.write("="*80 + "\n\n")

# ... [rest of the script] ...

save_contents_to_file(contents, 'extracted_contents.txt')
