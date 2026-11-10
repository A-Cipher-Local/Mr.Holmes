import requests
import xml.etree.ElementTree as ET

def extract_560_saint_germain():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print("[*] Downloading roll to pull complete details for Civic 560...")
    res = requests.get(url, timeout=90)
    root = ET.fromstring(res.content)
    
    for u in root.findall(".//RLUEx"):
        unit_map = {n.tag: n.text.strip() for n in u.iter() if n.text and n.text.strip()}
        
        civic = unit_map.get("RL0101Ax", "")
        street = unit_map.get("RL0101Gx", "").upper()
        
        if civic == "560" and "GERMAIN" in street:
            print("\n=======================================================")
            print("[+] MATCH VERIFIED: Primary Evaluation Record for Civic 560")
            print("=======================================================")
            print(f"  Civic Number  (RL0101Ax) : {civic}")
            print(f"  Street Type   (RL0101Ex) : {unit_map.get('RL0101Ex', 'N/A')}")
            print(f"  Street Name   (RL0101Gx) : {street}")
            print(f"  Land Value    (RL0402A)  : ${unit_map.get('RL0402A', '0')}")
            print(f"  Building Val  (RL0403A)  : ${unit_map.get('RL0403A', '0')}")
            print(f"  Total Value   (RL0404A)  : ${unit_map.get('RL0404A', '0')}")
            print(f"  Year Built    (RL0307A)  : {unit_map.get('RL0307A', 'N/A')}")
            print(f"  Usage Code    (RL0307B)  : {unit_map.get('RL0307B', 'N/A')}")
            
            print("\n  [Complete XML Tag Structure]:")
            for k, v in unit_map.items():
                print(f"    {k}: {v}")
            return

if __name__ == "__main__":
    extract_560_saint_germain()
