import json
import sys
import time
import requests

API_KEY = "YOUR_GOOGLE_API_KEY"
CX_ID = "YOUR_CUSTOM_SEARCH_ENGINE_ID"

def search_dork(query, api_key, cx):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cx
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[-] API Error [{response.status_code}]: {response.text}")
            return None
    except Exception as e:
        print(f"[-] Request failed: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 api_dorks.py <dork_query>")
        sys.exit(1)

    dork = sys.argv[1]
    print(f"[*] Querying API for: {dork}")
    
    data = search_dork(dork, API_KEY, CX_ID)
    if data and "items" in data:
        for idx, item in enumerate(data["items"], 1):
            print(f"\n[{idx}] {item.get('title')}")
            print(f"    Link: {item.get('link')}")
            print(f"    Snippet: {item.get('snippet')}")
    else:
        print("[-] No results returned or API limit reached.")

if __name__ == "__main__":
    main()
