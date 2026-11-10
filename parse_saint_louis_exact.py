import requests
import xml.etree.ElementTree as ET

def dump_exact_saint_louis():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print("[*] Downloading roll...")
    res = requests.get(url, timeout=90)
    root = ET.fromstring(res.content)
    units = root.findall(".//RLUEx")

    records = []
    for u in units:
        unit_map = {n.tag: n.text.strip() for n in u.iter() if n.text and n.text.strip()}
        st_name = unit_map.get("RL0101Gx", "").upper()
        
        if st_name == "SAINT-LOUIS":
            records.append({
                "civic": unit_map.get("RL0101Ax", ""),
                "type": unit_map.get("RL0101Ex", ""),
                "prefix": unit_map.get("RL0101Fx", ""),
                "dir": unit_map.get("RL0101Hx", ""),
                "total_val": unit_map.get("RL0404A", "0"),
                "land_val": unit_map.get("RL0402A", "0"),
                "bldg_val": unit_map.get("RL0403A", "0"),
                "year": unit_map.get("RL0307A", "N/A"),
                "usage": unit_map.get("RL0307B", "N/A"),
                "matricule": unit_map.get("RL0101", "N/A")
            })

    records.sort(key=lambda x: int(x['civic']) if x['civic'].isdigit() else 0)

    print(f"\n[+] Total Registered Properties on Rue Saint-Louis: {len(records)}")
    print("=" * 85)
    for r in records:
        print(f"Civic: {r['civic']:<5} {r['type']} {r['prefix']} SAINT-LOUIS {r['dir']:<2} | Total: ${r['total_val']:<9} | Built: {r['year']:<5} | Usage: {r['usage']:<2} | Matricule: {r['matricule']}")

if __name__ == "__main__":
    dump_exact_saint_louis()
