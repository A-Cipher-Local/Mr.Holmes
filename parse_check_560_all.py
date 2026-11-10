import csv
import requests
import xml.etree.ElementTree as ET

def find_exact_560_all_streets():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print("[*] Downloading roll to inspect ALL civic 560 units and street tags...")
    res = requests.get(url, timeout=90)
    root = ET.fromstring(res.content)
    units = root.findall(".//RLUEx")

    print(f"\n--- All 16 Properties with Civic '560' in Rimouski Roll ---")
    for u in units:
        unit_map = {n.tag: n.text.strip() for n in u.iter() if n.text and n.text.strip()}
        if unit_map.get("RL0101Ax") == "560":
            civic = unit_map.get("RL0101Ax", "")
            st_type = unit_map.get("RL0101Ex", "")
            st_prefix = unit_map.get("RL0101Fx", "")
            st_name = unit_map.get("RL0101Gx", "")
            st_dir = unit_map.get("RL0101Hx", "")
            
            print(f"  - Civic {civic} | Type: {st_type} | Prefix: {st_prefix} | Name: {st_name} | Dir: {st_dir}")
            print(f"    Valuation (RL0404A): ${unit_map.get('RL0404A', 'N/A')} | Year (RL0307A): {unit_map.get('RL0307A', 'N/A')} | Usage (RL0307B): {unit_map.get('RL0307B', 'N/A')}")
            print("    ---")

if __name__ == "__main__":
    find_exact_560_all_streets()
