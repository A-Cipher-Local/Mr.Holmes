import requests
import xml.etree.ElementTree as ET
import io

def parse_rimouski_target(xml_url, target_civic, target_street):
    print(f"[*] Downloading Rimouski 2026 roll XML...")
    res = requests.get(xml_url, timeout=90)
    if res.status_code != 200:
        print(f"[-] Download failed with status {res.status_code}")
        return

    print("[+] Download complete. Streaming XML elements...")
    
    # Parse stream to capture entire evaluation units
    context = ET.iterparse(io.BytesIO(res.content), events=("start", "end"))
    
    current_unit = {}
    found_count = 0

    for event, elem in context:
        if event == "start":
            # Tag values accumulate under current element
            if elem.text and elem.text.strip():
                current_unit[elem.tag] = elem.text.strip()
                
        elif event == "end":
            # Check unit boundary tags (e.g. RLU or similar property containers)
            if elem.tag in ["RLU", "UniteEvaluation", "Unite"]:
                civic = current_unit.get("RL0105A", "")
                street = current_unit.get("RL0107A", "").upper()
                
                # Check for civic number matching 560 and street containing ST-LOUIS / SAINT-LOUIS
                if civic == target_civic and any(kw in street for kw in [target_street, "ST-LOUIS", "SAINT LOUIS"]):
                    found_count += 1
                    print(f"\n==========================================")
                    print(f"[+] Found Match #{found_count}")
                    print(f"==========================================")
                    print(f"  - Civic Number (RL0105A) : {civic}")
                    print(f"  - Street Name   (RL0107A) : {current_unit.get('RL0107A', 'N/A')}")
                    print(f"  - Postal Code   (RL0109A) : {current_unit.get('RL0109A', 'N/A')}")
                    print(f"  - Land Value    (RL0402A) : ${current_unit.get('RL0402A', '0')}")
                    print(f"  - Building Val  (RL0403A) : ${current_unit.get('RL0403A', '0')}")
                    print(f"  - Total Value   (RL0404A) : ${current_unit.get('RL0404A', '0')}")
                    print(f"  - Year Built    (RL0307A) : {current_unit.get('RL0307A', 'N/A')}")
                    print(f"  - Usage Code    (RL0307B) : {current_unit.get('RL0307B', 'N/A')}")
                    
                    # Print raw record keys for full schema inspection
                    print("\n  [Raw Unit Fields]:")
                    for k, v in current_unit.items():
                        print(f"    {k}: {v}")
                
                # Reset unit state for next container
                current_unit = {}
            
            # Clear element memory buffer
            elem.clear()

    if found_count == 0:
        print(f"\n[-] No record found for civic '{target_civic}' on street '{target_street}'.")
        print("[*] Re-running fallback sweep for civic number only across entire document...")
        
        # Fallback check for civic 560 across all containers
        context = ET.iterparse(io.BytesIO(res.content), events=("end",))
        for event, elem in context:
            tags = {child.tag: child.text.strip() if child.text else "" for child in elem}
            if tags.get("RL0105A") == target_civic:
                print(f"\n[+] Fallback Match for Civic 560:")
                for k, v in tags.items():
                    if v:
                        print(f"    {k}: {v}")

if __name__ == "__main__":
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    parse_rimouski_target(url, "560", "SAINT-LOUIS")
