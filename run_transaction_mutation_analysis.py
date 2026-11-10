import requests
import xml.etree.ElementTree as ET

def analyze_2020_deed_mutation():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print("[*] Fetching roll to parse 2020 transaction metrics for Civic 560...")
    res = requests.get(url, timeout=90)
    if res.status_code != 200:
        print("[-] Download failed.")
        return

    root = ET.fromstring(res.content)
    
    for u in root.findall(".//RLUEx"):
        unit_map = {n.tag: n.text.strip() for n in u.iter() if n.text and n.text.strip()}
        
        civic = unit_map.get("RL0101Ax", "")
        street = unit_map.get("RL0101Gx", "").upper()
        
        if civic == "560" and "GERMAIN" in street:
            tx_date = unit_map.get("RL0201Gx", "N/A")
            reg_code = unit_map.get("RL0201Hx", "N/A")
            tx_type = unit_map.get("RL0201U", "N/A")
            curr_val = int(unit_map.get("RL0404A", "0"))
            prev_val = int(unit_map.get("RL0405A", "0"))
            delta = curr_val - prev_val
            pct = (delta / prev_val * 100) if prev_val > 0 else 0

            print("\n=======================================================")
            print("[+] Municipal Deed Transaction & Evaluation Audit")
            print("=======================================================")
            print(f"  Target Lot Number         (RL0103Ax) : {unit_map.get('RL0103Ax', 'N/A')}")
            print(f"  Deed Transaction Date     (RL0201Gx) : {tx_date}")
            print(f"  Registration Code         (RL0201Hx) : {reg_code}")
            print(f"  Transfer Type Category    (RL0201U)  : {tx_type}")
            print(f"  Current Assessment Base  (RL0404A)  : ${curr_val:,}")
            print(f"  Prior Assessment Base    (RL0405A)  : ${prev_val:,}")
            print(f"  Net Assessment Shift                 : +${delta:,} (+{pct:.1f}%)")
            return

if __name__ == "__main__":
    analyze_2020_deed_mutation()
