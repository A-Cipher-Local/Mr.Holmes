import os
import re

cache_dir = "intel_cache"
print("[*] Scanning local intel_cache/ for webhooks, IPs, and endpoints:\n")

url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')

for filename in os.listdir(cache_dir):
    filepath = os.path.join(cache_dir, filename)
    if os.path.isfile(filepath):
        print(f"=== File: {filename} ===")
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, 1):
                # Search for webhooks or API URLs
                matches = url_pattern.findall(line)
                if matches:
                    for m in matches:
                        print(f"  Line {line_no}: {m}")
                # Search for keywords like webhook, token, api, or discord
                elif any(kw in line.lower() for kw in ["webhook", "token", "discord", "api", "identifier"]):
                    print(f"  Line {line_no} [Keyword Hit]: {line.strip()}")
        print()
