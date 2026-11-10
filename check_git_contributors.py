import urllib.request
import json

url = "https://api.github.com/repos/KeemStar58/mobile-app/contributors"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github.v3+json"
}

print("[*] Querying public contributor metadata for KeemStar58/mobile-app...")
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode("utf-8"))
        for user in data:
            print(f"  [+] Contributor: {user.get('login')} (Profile: {user.get('html_url')})")
except Exception as e:
    print(f"[-] Target repo may be private or rate-limited: {e}")
