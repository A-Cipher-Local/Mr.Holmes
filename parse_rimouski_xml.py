import requests
import xml.etree.ElementTree as ET

def parse_rimouski_roll():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print(f"[*] Downloading Rimouski 2026 Assessment Roll XML...")
    
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            print("[+] Download complete. Parsing XML tree...")
            root = ET.fromstring(response.content)
            
            matches = 0
            # Iterate through elements to locate matching property nodes
            for elem in root.iter():
                # Aggregate text in the element subtree to check for target address components
                subtree_text = "".join(elem.itertext())
                if "560" in subtree_text and ("SAINT-LOUIS" in subtree_text.upper() or "ST-LOUIS" in subtree_text.upper()):
                    matches += 1
                    print(f"\n[+] Match Found (#{matches}):")
                    # Print relevant child fields or text snippet
                    for child in elem:
                        if child.text:
                            print(f"  - {child.tag}: {child.text.strip()}")
            
            if matches == 0:
                print("[-] No exact nodes matched '560' and 'Saint-Louis' in this pass. Inspecting broader structure...")
        else:
            print(f"[-] Download failed with status code: {response.status_code}")
    except Exception as e:
        print(f"[!] Error parsing XML: {e}")

if __name__ == "__main__":
    parse_rimouski_roll()
