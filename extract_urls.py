import json
import re
from urllib.parse import urlparse

with open("brand_dork_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

unique_urls = set()
unique_domains = set()

for target, queries in data.items():
    for q, results in queries.items():
        for r in results:
            url = r.get("href")
            if url:
                unique_urls.add(url)
                parsed = urlparse(url)
                if parsed.netloc:
                    unique_domains.add(parsed.netloc)

print(f"[+] Total Unique URLs Extracted: {len(unique_urls)}")
print(f"[+] Total Unique Domains: {len(unique_domains)}\n")

with open("unique_urls.txt", "w", encoding="utf-8") as f_url:
    for u in sorted(unique_urls):
        f_url.write(u + "\n")

with open("unique_domains.txt", "w", encoding="utf-8") as f_dom:
    for d in sorted(unique_domains):
        f_dom.write(d + "\n")

print("[+] Saved clean lists to unique_urls.txt and unique_domains.txt")
