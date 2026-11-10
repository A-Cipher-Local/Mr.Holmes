import urllib.request
import json

targets = ["DramaAlert", "Keemstar", "HappyPunch"]
platforms = {
    "GitHub": "https://github.com/{}",
    "X (Twitter)": "https://x.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Pastebin User": "https://pastebin.com/u/{}"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("[*] Running stealth endpoint verification...")

for target in targets:
    print(f"\n--- Checking Target: {target} ---")
    for platform, url_template in platforms.items():
        target_url = url_template.format(target)
        req = urllib.request.Request(target_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    print(f"  [+] [ACTIVE] {platform}: {target_url}")
        except Exception as e:
            # Silently catch 404s or blocks to maintain stealth
            pass
