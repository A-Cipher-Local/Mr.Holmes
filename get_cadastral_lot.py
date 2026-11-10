import requests

def fetch_cadastral_lot():
    # Public ArcGIS REST Endpoint for Quebec Cadastre (MRNF)
    url = "https://servicesgeographiques.mrnf.gouv.qc.ca/arcgis/rest/services/Cadastre/CadastreQuebecPublic/MapServer/find"
    
    params = {
        "searchText": "560 rue Saint-Louis-Ouest Rimouski",
        "contains": "true",
        "searchFields": "ADRESSE, NOM_RUE",
        "layers": "0",  # Parcel / Lot layer
        "f": "json"
    }
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print("[*] Querying Quebec MRNF Cadastral GIS Endpoint...")
    try:
        res = requests.get(url, params=params, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            results = data.get("results", [])
            print(f"[+] Found {len(results)} spatial matches.")
            for r in results:
                attrs = r.get("attributes", {})
                print(f"  - Lot Number (LOT) : {attrs.get('NO_LOT', 'N/A')}")
                print(f"  - Address Match   : {attrs.get('ADRESSE', 'N/A')}")
                print(f"  - Municipality    : {attrs.get('MUNICI PALITE', 'Rimouski')}")
        else:
            print(f"[-] GIS Request failed with HTTP {res.status_code}")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    fetch_cadastral_lot()
