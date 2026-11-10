import urllib.request
import os

os.makedirs("intel_cache", exist_ok=True)
files_to_grab = {
    "hp_client.lua": "https://raw.githubusercontent.com/HappyPunch/hp-reports/main/source/client.lua",
    "hp_config.lua": "https://raw.githubusercontent.com/HappyPunch/hp-reports/main/sv_config.lua"
}

headers = {"User-Agent": "Mozilla/5.0"}

for name, url in files_to_grab.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            content = response.read().decode("utf-8")
            with open(os.path.join("intel_cache", name), "w", encoding="utf-8") as f:
                f.write(content)
        print(f"[+] Downloaded and cached: {name}")
    except Exception as e:
        print(f"[-] Could not fetch {name}: {e}")
