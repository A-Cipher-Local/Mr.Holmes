import requests

def query_rimouski_api():
    # MAMH API endpoint for municipal evaluation units
    base_url = "https://donneesouvertes.affmunqc.net/api/v1/role/10043/units"
    params = {
        "civic": "560",
        "street": "SAINT-LOUIS",
        "limit": 50
    }
    
    print("[*] Querying MAMH provincial API endpoint for Rimouski (10043)...")
    try:
        response = requests.get(base_url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"[+] API Response Received: {data}")
        else:
            print(f"[-] Direct API returned HTTP {response.status_code}. Endpoint requires direct matricule key.")
    except Exception as e:
        print(f"[-] API request error: {e}")

if __name__ == "__main__":
    query_rimouski_api()
