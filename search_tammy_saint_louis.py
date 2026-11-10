import requests
import xml.etree.ElementTree as ET

def search_owner_tammy():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print("[*] Downloading and scanning Rimouski 2026 roll for owner 'Tammy'...")
    res = requests.get(url, timeout=90)
    if res.status_code != 200:
        print("[-] Download failed.")
        return

    root = ET.fromstring(res.content)
    units = root.findall(".//RLUEx")
    print(f"[+] Loaded {len(units)} total evaluation units.")

    st_louis_tammy_matches = []
    global_tammy_matches = []

    for u in units:
        unit_map = {}
        for node in u.iter():
            if node.tag and node.text and node.text.strip():
                unit_map[node.tag] = node.text.strip()

        # Gather all text values from the unit to check for "TAMMY"
        full_text_block = " ".join(unit_map.values()).upper()
        
        if "TAMMY" in full_text_block:
            civic = unit_map.get("RL0101Ax", "N/A")
            street = f"{unit_map.get('RL0101Ex', '')} {unit_map.get('RL0101Fx', '')} {unit_map.get('RL0101Gx', '')} {unit_map.get('RL0101Hx', '')}".strip()
            
            record = {
                "civic": civic,
                "street": street,
                "total_val": unit_map.get("RL0404A", "0"),
                "year": unit_map.get("RL0307A", "N/A"),
                "matricule": unit_map.get("RL0101", "N/A"),
                "raw_tags": unit_map
            }

            if "LOUIS" in street:
                st_louis_tammy_matches.append(record)
            else:
                global_tammy_matches.append(record)

    print("\n========================================================")
    print(f"[+] Matches on Street SAINT-LOUIS for 'Tammy': {len(st_louis_tammy_matches)}")
    print("========================================================")
    for r in st_louis_tammy_matches:
        print(f"  Civic: {r['civic']} | Street: {r['street']} | Matricule: {r['matricule']}")
        print(f"  Total Value: ${r['total_val']} | Year Built: {r['year']}")
        print("  Full Name / Owner Text Fields:")
        for k, v in r['raw_tags'].items():
            if "TAMMY" in v.upper():
                print(f"    [{k}]: {v}")
        print("-" * 55)

    print("\n========================================================")
    print(f"[+] Global Matches in Rimouski Roll for 'Tammy': {len(global_tammy_matches)}")
    print("========================================================")
    for r in global_tammy_matches:
        print(f"  Civic: {r['civic']} | Street: {r['street']} | Matricule: {r['matricule']}")
        print("  Full Name / Owner Text Fields:")
        for k, v in r['raw_tags'].items():
            if "TAMMY" in v.upper():
                print(f"    [{k}]: {v}")
        print("-" * 55)

if __name__ == "__main__":
    search_owner_tammy()
