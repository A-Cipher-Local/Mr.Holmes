import requests

def query_quebec_open_data(address, city=""):
    full_query = f"{address} {city}".strip()
    print(f"[*] Querying Données Québec for: '{full_query}'...")
    
    api_url = "https://www.donneesquebec.ca/recherche/api/3/action/datastore_search"
    resource_id = "1f30b9d7-e244-42f7-b08e-5b6eb9e663a0"
    params = {"resource_id": resource_id, "q": full_query, "limit": 10}
    
    try:
        r = requests.get(api_url, params=params, timeout=10)
        data = r.json()
        records = data.get("result", {}).get("records", [])
        
        if records:
            print(f"[+] Found {len(records)} matching corporate record(s):")
            for rec in records:
                neq = rec.get('NEQ', 'N/A')
                name = rec.get('NOM_ENTR', 'N/A')
                status = rec.get('STAT_IMMAT', 'N/A')
                print(f"  - NEQ: {neq} | Name: {name} | Status: {status}")
        else:
            print(f"[-] No business entities found registered for '{full_query}'.")
            
    except Exception as e:
        print(f"[!] Request error: {e}")

if __name__ == "__main__":
    municipalities = ["Rimouski", "Saint-Jean-sur-Richelieu", "Gatineau"]
    base_address = "560 rue Saint-Louis-Ouest"
    
    for city in municipalities:
        query_quebec_open_data(base_address, city)
        print("-" * 50)
