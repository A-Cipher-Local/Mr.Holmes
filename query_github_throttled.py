import urllib.request
import urllib.parse
import json
import time
import sys

TARGET_MAP = {
    "stlawrenceparish": [
        "stlawrenceparish", "st lawrence parish"
    ],
    "DemonSmooch": [
        "DemonSmooch", "demonsmooch"
    ],
    "TammyBUsagi": [
        "TammyBUsagi", "tammybusagi"
    ],
    "Hannaki": [
        "Hannaki"
    ],
    "lukege287": [
        "lukege287@gmail.com", "lukege287"
    ],
    "IsaacGuest_Group": [
        "IsaacGuest", "BeMyGuest", "GuestMob"
    ],
    "Keemstar_Group": [
        "Keemstar", "DramaAlert", "keem llc"
    ],
    "KBAC_Group": [
        "Mike Greene", "KBAC", "kid behind the camera"
    ],
    "AlyssaBrantly": [
        "Alyssa Haleigh Brantly", "alyssahaleigh"
    ],
    "TechProtect": [
        "TechProtect", "techprotect"
    ],
    "SourPower": [
        "SourPower", "sourpower"
    ],
    "Boogie2988": [
        "Boogie2988", "steven williams"
    ],
    "Khan_Group": [
        "Khan.MVP", "KhanMp"
    ],
    "KenCaint": [
        "KenCaint", "kencaint"
    ],
    "M1nty_Group": [
        "M1nty", "minty steve"
    ],
    "ZitaRae_Group": [
        "ZitaRaeAllDay", "Zita Rae"
    ],
    "Lolcow_Communities": [
        "lolcowuncensored", "lolcow china"
    ]
}

<<<<<<< HEAD
TOKEN = "YOUR_TOKEN_HERE"
=======
TOKEN = "YOUR_GITHUB_TOKEN"
>>>>>>> 39f90d6 (chore: sanitize hardcoded tokens and update core OSINT modules)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-Tool/1.0",
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {TOKEN}"
}

def main():
    print(f"[*] Starting throttled reconnaissance sweep...")
    
    for category, terms in TARGET_MAP.items():
        print(f"\n[-] Category: {category}")
        for term in terms:
            encoded = urllib.parse.quote(term)
            url = f"https://api.github.com/search/code?q={encoded}"
            print(f"    [->] Querying: '{term}'...", end="", flush=True)
            
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=12) as response:
                    data = json.loads(response.read().decode())
                    total = data.get("total_count", 0)
                    print(f" Hits: {total}")
                    for item in data.get("items", [])[:1]:
                        repo = item.get('repository', {}).get('full_name', 'N/A')
                        print(f"        -> Top Match: {repo}")
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    print(f" [Rate Limited / Forbidden]")
                    print(f"        [*] Sleeping 10 seconds to bypass secondary throttle...")
                    time.sleep(10)
                else:
                    print(f" [HTTP {e.code}]")
            except Exception as e:
                print(f" [Error: {e}]")
            
            # Mandatory pacing delay to respect GitHub API search limits
            time.sleep(3.5)

if __name__ == "__main__":
    main()
