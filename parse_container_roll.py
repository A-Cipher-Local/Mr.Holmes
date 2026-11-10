import requests
import xml.etree.ElementTree as ET
import io

def parse_container_schema(xml_url, target_civic, target_street_keyword):
    print(f"[*] Downloading and parsing Rimouski XML roll...")
    res = requests.get(xml_url, timeout=90)
    if res.status_code != 200:
        print("[-] Download failed.")
        return

    root = ET.fromstring(res.content)
    found = 0

    # Iterate through all parent elements in the XML tree
    for parent in root.iter():
        civic = ""
        street_name = ""
        unit_tags = {}
        
        # Scan all descendants of this parent container to aggregate property attributes
        for elem in parent.iter():
            if elem.tag and elem.text and elem.text.strip():
                unit_tags[elem.tag] = elem.text.strip()

        civic = unit_tags.get("RL0101Ax", "")
        street_name = unit_tags.get("RL0101Gx", "").upper()

        # Check if this container holds our target address
        if civic == target_civic and target_street_keyword in street_name:
            found += 1
            print(f"\n==========================================")
            print(f"[+] Container Property Match Found #{found}")
            print(f"==========================================")
            print(f"  - Civic Number (RL0101Ax) : {civic}")
            print(f"  - Street Type  (RL0101Ex) : {unit_tags.get('RL0101Ex', 'N/A')}")
            print(f"  - Street Name  (RL0101Gx) : {street_name}")
            print(f"  - Land Value   (RL0402A)  : ${unit_tags.get('RL0402A', '0')}")
            print(f"  - Building Val (RL0403A)  : ${unit_tags.get('RL0403A', '0')}")
            print(f"  - Total Value  (RL0404A)  : ${unit_tags.get('RL0404A', '0')}")
            print(f"  - Year Built   (RL0307A)  : {unit_tags.get('RL0307A', 'N/A')}")
            print(f"  - Usage Code   (RL0307B)  : {unit_tags.get('RL0307B', 'N/A')}")
            
            print("\n  [Full Container Raw Attributes]:")
            for k, v in unit_tags.items():
                if v:
                    print(f"    {k}: {v}")

    if found == 0:
        print(f"\n[-] No container matched civic '{target_civic}' with street keyword '{target_street_keyword}'.")

if __name__ == "__main__":
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    parse_container_schema(url, "560", "LOUIS")
