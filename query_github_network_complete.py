import urllib.request
import urllib.parse
import json

# Complete investigation target mapping including all entities, variations, network connections, and final additions
TARGET_MAP = {
    "stlawrenceparish": [
        "stlawrenceparish", "st lawrence parish", "stlawrence parish"
    ],
    "DemonSmooch": [
        "DemonSmooch", "demon smooch", "demonsmooch"
    ],
    "TammyBUsagi": [
        "TammyBUsagi", "tammy busagi", "tammybusagi"
    ],
    "Hannaki": [
        "Hannaki", "hannaki"
    ],
    "lukege287": [
        "lukege287@gmail.com", "lukege287"
    ],
    "IsaacGuest_Group": [
        "IsaacGuest", "isaac guest", "BeMyGuest", "GuestMob", "bemyguest", "guestmob"
    ],
    "Keemstar_Group": [
        "Keemstar", "Keem", "DramaAlert", "dramaalert", "keem llc", "keem"
    ],
    "KBAC_Group": [
        "Mike Greene", "KBAC", "kid behind the camera", "kidbehindthecamera", "kbac", "family convention"
    ],
    "AlyssaBrantly": [
        "Alyssa Haleigh Brantly", "alyssa brantly", "alyssahaleigh"
    ],
    "TechProtect": [
        "TechProtect", "tech protect", "techprotect"
    ],
    "SourPower": [
        "SourPower", "sour power", "sourpower"
    ],
    "Boogie2988": [
        "Boogie2988", "boogie 2988", "boogie2988", "steven williams"
    ],
    "Khan_Group": [
        "Khan.MVP", "KhanMp", "khanmvp", "khanmp", "khan mvp", "khan mp"
    ],
    "KenCaint": [
        "KenCaint", "kencaint", "ken caint"
    ],
    "M1nty_Group": [
        "M1nty", "m1nty", "minty", "minty steve", "m1nty steve"
    ],
    "ZitaRae_Group": [
        "ZitaRaeAllDay", "zita rae all day", "Zita Rae", "zitarae", "zitaraeallday"
    ],
    "Lolcow_Communities": [
        "lolcowuncensored", "lolcow uncensored", "lolcow china", "lolcowchina", "lolcow podcast"
    ],
    "Related_Connections": [
        "fouseytube", "prilly", "epic meal time", "ssundee", "minecraft server host"
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
    total_queries = sum(len(v) for v in TARGET_MAP.values())
    print(f"[*] Executing {total_queries} queries across {len(TARGET_MAP)} target and connection categories...")
    
    for category, terms in TARGET_MAP.items():
        print(f"\n========================================")
        print(f"[*] Category Matrix: {category}")
        print(f"========================================")
        for term in terms:
            encoded = urllib.parse.quote(term)
            url = f"https://api.github.com/search/code?q={encoded}"
            print(f"\n    [->] Searching term: '{term}'")
            
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=12) as response:
                    data = json.loads(response.read().decode())
                    total = data.get("total_count", 0)
                    print(f"         Results found: {total}")
                    for item in data.get("items", [])[:2]:
                        repo = item.get('repository', {}).get('full_name', 'N/A')
                        path = item.get('path', 'N/A')
                        print(f"           - Repo: {repo} | File: {path}")
            except urllib.error.HTTPError as e:
                print(f"         HTTP Error {e.code}: {e.reason}")
            except Exception as e:
                print(f"         Error: {e}")

if __name__ == "__main__":
    main()
