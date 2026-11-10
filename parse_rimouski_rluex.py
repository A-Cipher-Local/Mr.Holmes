import requests
import xml.etree.ElementTree as ET

def extract_rimouski_property():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print("[*] Downloading Rimouski 2026 assessment roll XML...")
    res = requests.get(url, timeout=90)
    if res.status_code != 200:
        print(f"[-] Download failed (Status: {res.status_code})")
        return

    print("[+] Parsing XML tree...")
    root = ET.fromstring(res.content)
    
    units = root.findall(".//RLUEx")
    print(f"[+] Total RLUEx units: {len(units)}")
    
    matches = 0
    for u in units:
        # Collect all key-value text tags inside this single evaluation unit
        unit_map = {}
        for node in u.iter():
            if node.tag and node.text and node.text.strip():
                unit_map[node.tag] = node.text.strip()
        
        civic = unit_map.get("RL0101Ax", "")
        street = unit_map.get("RL0101Gx", "").upper()
        
        # Match civic number 560 and street containing LOUIS
        if civic == "560" and "LOUIS" in street:
            matches += 1
            print(f"\n==========================================")
            print(f"[+] Property Record Found #{matches}")
            print(f"==========================================")
            print(f"  Civic Number  (RL0101Ax) : {civic}")
            print(f"  Street Type   (RL0101Ex) : {unit_map.get('RL0101Ex', 'N/A')}")
            print(f"  Street Name   (RL0101Gx) : {street}")
            print(f"  Land Value    (RL0402A)  : ${unit_map.get('RL0402A', '0')}")
            print(f"  Building Val  (RL0403A)  : ${unit_map.get('RL0403A', '0')}")
            print(f"  Total Value   (RL0404A)  : ${unit_map.get('RL0404A', '0')}")
            print(f"  Year Built    (RL0307A)  : {unit_map.get('RL0307A', 'N/A')}")
            print(f"  Usage Code    (RL0307B)  : {unit_map.get('RL0307B', 'N/A')}")
            
            print("\n  [Full Extracted Unit Tags]:")
            for k, v in unit_map.items():
                print(f"    {k}: {v}")

    if matches == 0:
        print("\n[-] No match found under street 'LOUIS'. Listing all street names for civic 560:")
        for u in units:
            unit_map = {n.tag: n.text.strip() for n in u.iter() if n.text and n.text.strip()}
            if unit_map.get("RL0101Ax") == "560":
                print(f"  - 560 {unit_map.get('RL0101Ex', '')} {unit_map.get('RL0101Gx', '')}")

if __name__ == "__main__":
    extract_rimouski_property()
