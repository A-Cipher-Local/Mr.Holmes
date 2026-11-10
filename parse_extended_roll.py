import requests
import xml.etree.ElementTree as ET
import io

def parse_extended_schema(xml_url, target_civic, target_street_keyword):
    print(f"[*] Downloading and parsing Rimouski XML roll...")
    res = requests.get(xml_url, timeout=90)
    if res.status_code != 200:
        print("[-] Download failed.")
        return

    root = ET.fromstring(res.content)
    found = 0

    # Search through the document for RL0101x nodes containing the civic number
    for parent in root.iter():
        # Check if this node or its children contain the target civic number and street name
        civic = ""
        street_name = ""
        
        # Build dictionary of child tags for this element block
        block_data = {}
        for child in parent:
            val = child.text.strip() if child.text else ""
            block_data[child.tag] = val

        civic = block_data.get("RL0101Ax", "")
        street_name = block_data.get("RL0101Gx", "").upper()

        if civic == target_civic and target_street_keyword in street_name:
            found += 1
            print(f"\n==========================================")
            print(f"[+] Exact Property Match Found #{found}")
            print(f"==========================================")
            print(f"  - Civic Number (RL0101Ax) : {civic}")
            print(f"  - Street Type  (RL0101Ex) : {block_data.get('RL0101Ex', 'N/A')}")
            print(f"  - Street Name  (RL0101Gx) : {street_name}")
            
            # Let's search sibling/parent scopes for property valuation metrics
            # In XML trees, evaluation amounts (RL040x) reside in adjacent nodes under the same parent unit
            print("\n  [Associated Valuation & Structure Data]:")
            for elem in root.iter():
                sub_tags = {c.tag: c.text.strip() if c.text else "" for c in elem}
                if sub_tags.get("RL0101Ax") == target_civic and "RL0404A" in sub_tags:
                    for k, v in sub_tags.items():
                        if v:
                            print(f"    {k}: {v}")

    if found == 0:
        print(f"\n[-] No record found for civic '{target_civic}' matching street keyword '{target_street_keyword}'.")

if __name__ == "__main__":
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    parse_extended_schema(url, "560", "LOUIS")
