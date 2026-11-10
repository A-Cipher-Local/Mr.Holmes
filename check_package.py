import requests

def inspect_package(package_id):
    url = f"https://www.donneesquebec.ca/recherche/api/3/action/package_show?id={package_id}"
    print(f"[*] Fetching metadata for package: {package_id}")
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("success"):
            resources = data["result"]["resources"]
            print(f"[+] Total resources in package: {len(resources)}")
            for i, res in enumerate(resources):
                name = res.get("name", "Unnamed")
                fmt = res.get("format", "N/A")
                rid = res.get("id", "N/A")
                active = res.get("datastore_active", False)
                print(f"  [{i+1}] Name: {name} | Format: {fmt} | Active DS: {active}")
                print(f"      ID: {rid}")
        else:
            print("[-] Failed to retrieve package metadata.")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    inspect_package("role-evaluation-fonciere-du-quebec")
