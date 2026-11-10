import requests
import xml.etree.ElementTree as ET

def parse_inside_and_outside_local(xml_url):
    print("[*] Downloading Rimouski 2026 assessment roll XML...")
    res = requests.get(xml_url, timeout=90)
    if res.status_code != 200:
        print("[-] Download failed.")
        return

    print("[+] Parsing evaluation units...")
    root = ET.fromstring(res.content)
    units = root.findall(".//RLUEx")
    print(f"[+] Total units loaded: {len(units)}")

    # 1. Inside Local: Upper-bound civics directly on SAINT-LOUIS (Civic >= 300)
    inside_local_matches = []
    
    # 2. Outside Local: Cross-reference properties on primary intersecting arteries (e.g., SAINT-GERMAIN)
    # that sit in the 500-600 civic range near the Saint-Louis sector boundary
    outside_local_matches = []

    for u in units:
        unit_map = {node.tag: node.text.strip() for node in u.iter() if node.text and node.text.strip()}
        
        st_name = unit_map.get("RL0101Gx", "").upper()
        civic_raw = unit_map.get("RL0101Ax", "")
        civic_num = int(civic_raw) if civic_raw.isdigit() else 0

        # Inside Local Check
        if st_name == "SAINT-LOUIS" and civic_num >= 300:
            inside_local_matches.append({
                "civic": civic_raw,
                "type": unit_map.get("RL0101Ex", ""),
                "street": st_name,
                "matricule": unit_map.get("RL0101", "N/A"),
                "total_val": unit_map.get("RL0404A", "0"),
                "year": unit_map.get("RL0307A", "N/A"),
                "use": unit_map.get("RL0307B", "N/A")
            })

        # Outside Local Check (Nearby anchor street in the 500-600 civic range)
        if "SAINT-GERMAIN" in st_name and 550 <= civic_num <= 570:
            outside_local_matches.append({
                "civic": civic_raw,
                "type": unit_map.get("RL0101Ex", ""),
                "street": st_name,
                "matricule": unit_map.get("RL0101", "N/A"),
                "total_val": unit_map.get("RL0404A", "0"),
                "year": unit_map.get("RL0307A", "N/A"),
                "use": unit_map.get("RL0307B", "N/A")
            })

    # Output Inside Local
    print("\n==================================================================")
    print(" [INSIDE LOCAL] Primary Registered Parcels on Saint-Louis (300+)")
    print("==================================================================")
    inside_local_matches.sort(key=lambda x: int(x['civic']) if x['civic'].isdigit() else 0)
    for m in inside_local_matches:
        print(f"  Civic {m['civic']:<4} {m['type']} {m['street']} | Valuation: ${m['total_val']:<9} | Built: {m['year']} | Matricule: {m['matricule']}")

    # Output Outside Local
    print("\n==================================================================")
    print(" [OUTSIDE LOCAL] Intersecting Commercial/Anchor Parcels (550-570 Range)")
    print("==================================================================")
    outside_local_matches.sort(key=lambda x: int(x['civic']) if x['civic'].isdigit() else 0)
    for m in outside_local_matches:
        print(f"  Civic {m['civic']:<4} {m['type']} {m['street']} | Valuation: ${m['total_val']:<9} | Built: {m['year']} | Matricule: {m['matricule']}")

if __name__ == "__main__":
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    parse_inside_and_outside_local(url)
