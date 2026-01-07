import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json

def crawl_website(start_url, max_pages=10):
    visited = set()
    to_visit = [start_url]
    pages = {}
    site_graph = {}

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            res = requests.get(url, timeout=10)
            html = res.text
        except Exception:
            continue

        visited.add(url)

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)
        pages[url] = text

        path = urlparse(url).path or "/"
        site_graph[path] = []

        for a in soup.find_all("a", href=True):
            full = urljoin(start_url, a["href"])
            if urlparse(full).netloc == urlparse(start_url).netloc:
                if full not in visited and full not in to_visit:
                    to_visit.append(full)
                link_path = urlparse(full).path or "/"
                if link_path not in site_graph[path]:
                    site_graph[path].append(link_path)

        time.sleep(0.3)

    with open("pages.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)

    with open("site_map.json", "w", encoding="utf-8") as f:
        json.dump(site_graph, f, indent=2, ensure_ascii=False)

    return pages, site_graph


if __name__ == "__main__":
    url = input("Enter Website URL to crawl: ")
    crawl_website(url, max_pages=10)
    print("Crawling completed! Files saved → pages.json & site_map.json")
