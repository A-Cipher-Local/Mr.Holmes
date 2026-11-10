import requests
import csv
import io

def fetch_evaluation_index():
    resource_id = "c0e65c47-fcc1-40e4-bc2e-7baa74bc164a"
    metadata_url = f"https://www.donneesquebec.ca/recherche/api/3/action/resource_show?id={resource_id}"
    
    print("[*] Fetching resource download link from Données Québec API...")
    try:
        res = requests.get(metadata_url, timeout=10).json()
        if res.get("success"):
            download_url = res["result"]["url"]
            print(f"[+] Download URL acquired: {download_url}")
            
            print("[*] Downloading CSV index table...")
            csv_data = requests.get(download_url, timeout=30).content
            
            # Parse using built-in csv module
            f = io.StringIO(csv_data.decode('utf-8', errors='ignore'))
            reader = csv.DictReader(f)
            rows = list(reader)
            
            print(f"[+] Loaded index containing {len(rows)} rows.")
            if rows:
                print(f"[*] Available Columns: {list(rows[0].keys())}")
            
            return rows
        else:
            print("[-] Failed to retrieve resource metadata.")
    except Exception as e:
        print(f"[!] Error: {e}")
    return None

if __name__ == "__main__":
    rows = fetch_evaluation_index()
    if rows:
        matches = []
        for row in rows:
            row_str = " ".join(str(v) for v in row.values())
            if any(term in row_str for term in ["Rimouski", "Gatineau", "Saint-Jean"]):
                matches.append(row)
        
        print(f"\n[+] Matching Municipal Index Entries ({len(matches)} found):")
        for m in matches[:10]:
            print(m)
