import requests
import xml.etree.ElementTree as ET

def find_saint_louis_properties():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print("[*] Downloading and scanning Rimouski 2026 XML roll...")
    res = requests.get(url, timeout=90)
    if res.status_code != 200:
        print("[-] Download failed.")
        return

    root = ET.fromstring(res.content)
    units = root.findall(".//RLUEx")
    print(f"[+] Total units scanned: {len(units)}")

    st_louis_matches = []

    for u in units:
        unit_map = {n.tag: n.text.strip() for n in u.iter() if n.text and n.text.strip()}
        
        street_name = unit_map.get("RL0101Gx", "").upper()
        street_type = unit_map.get("RL0101Ex", "").upper()
        civic = unit_map.get("RL0101Ax", "")

        # Match any property on Saint-Louis / St-Louis
        if "LOUIS" in street_name:
            st_louis_matches.append({
                "civic": civic,
                "type": street_type,
                "street": street_name,
                "land_val": unit_map.get("RL0402A", "0"),
                "bldg_val": unit_map.get("RL0403A", "0"),
                "total_val": unit_map.get("RL0404A", "0"),
                "year_built": unit_map.get("RL0307A", "N/A"),
                "use_code": unit_map.get("RL0307B", "N/A")
            })

    print(f"\n[+] Total properties found on Saint-Louis: {len(st_louis_matches)}")
    
    # Sort by civic number for easy scanning
    st_louis_matches.sort(key=lambda x: int(x['civic']) if x['civic'].isdigit() else 0)
    
    print("\n--- Civic Numbers Registered on Street LOUIS ---")
    for prop in st_louis_matches:
        if 500 <= (int(prop['civic']) if prop['civic'].isdigit() else 0) <= 620:
            print(f"  - Civic {prop['civic']} {prop['type']} {prop['street']} | Total: ${prop['total_val']} | Built: {prop['year_built']}")

if __name__ == "__main__":
    find_saint_louis_properties()
