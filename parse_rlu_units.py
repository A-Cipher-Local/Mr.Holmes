import requests
import xml.etree.ElementTree as ET
import io

def parse_rimouski_rlu(xml_url, target_civic, target_street):
    print(f"[*] Fetching and parsing Rimouski XML roll...")
    res = requests.get(xml_url, timeout=90)
    if res.status_code != 200:
        print(f"[-] Download failed with status {res.status_code}")
        return

    root = ET.fromstring(res.content)
    found = 0

    # Locate all top-level property evaluation units (RLU)
    units = root.findall(".//RLU")
    print(f"[+] Loaded {len(units)} total evaluation units from roll.")

    for u in units:
        # Extract all child tag key-value pairs inside this single RLU unit
        unit_tags = {}
        for child in u.iter():
            if child.tag and child.text and child.text.strip():
                unit_tags[child.tag] = child.text.strip()

        # Check civic number (RL0101Ax or RL0105A) and street name (RL0101Gx or RL0107A)
        civic = unit_tags.get("RL0101Ax") or unit_tags.get("RL0105A") or ""
        street = (unit_tags.get("RL0101Gx") or unit_tags.get("RL0107A") or "").upper()

        if civic == target_civic and target_street.upper() in street:
            found += 1
            print(f"\n==========================================")
            print(f"[+] Exact RLU Property Match Found #{found}")
            print(f"==========================================")
            print(f"  - Civic Number (RL0101Ax) : {civic}")
            print(f"  - Street Type  (RL0101Ex) : {unit_tags.get('RL0101Ex', 'N/A')}")
            print(f"  - Street Name  (RL0101Gx) : {street}")
            print(f"  - Land Value   (RL0402A)  : ${unit_tags.get('RL0402A', '0')}")
            print(f"  - Building Val (RL0403A)  : ${unit_tags.get('RL0403A', '0')}")
            print(f"  - Total Value  (RL0404A)  : ${unit_tags.get('RL0404A', '0')}")
            print(f"  - Year Built   (RL0307A)  : {unit_tags.get('RL0307A', 'N/A')}")
            print(f"  - Usage Code   (RL0307B)  : {unit_tags.get('RL0307B', 'N/A')}")
            
            print("\n  [All Unit Tags]:")
            for k, v in unit_tags.items():
                print(f"    {k}: {v}")

    if found == 0:
        print(f"\n[-] No RLU unit matched civic '{target_civic}' with street keyword '{target_street}'.")
        print("[*] Printing unique street names found across all civic 560 units:")
        for u in units:
            unit_tags = {c.tag: c.text.strip() for c in u.iter() if c.text and c.text.strip()}
            civic = unit_tags.get("RL0101Ax") or unit_tags.get("RL0105A")
            if civic == target_civic:
                st = unit_tags.get("RL0101Gx") or unit_tags.get("RL0107A")
                st_type = unit_tags.get("RL0101Ex") or ""
                print(f"  - Civic 560 on: {st_type} {st}")

if __name__ == "__main__":
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    parse_rimouski_rlu(url, "560", "LOUIS")
