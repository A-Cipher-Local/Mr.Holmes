import requests

def search_packages(query):
    url = "https://www.donneesquebec.ca/recherche/api/3/action/package_search"
    params = {"q": query, "rows": 5}
    
    try:
        res = requests.get(url, params=params, timeout=10).json()
        if res.get("success"):
            results = res["result"]["results"]
            print(f"[+] Found {len(results)} package(s) matching '{query}':")
            for pkg in results:
                print(f"  - Title: {pkg.get('title')}")
                print(f"    Name/ID: {pkg.get('name')}")
                print(f"    Resources: {len(pkg.get('resources', []))}")
                for r in pkg.get('resources', [])[:3]:
                    print(f"      * [{r.get('format')}] {r.get('name')} ({r.get('id')})")
        else:
            print("[-] Search failed.")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    search_packages("rôle d'évaluation foncière")
