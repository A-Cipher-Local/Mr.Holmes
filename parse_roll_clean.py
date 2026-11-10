import xml.etree.ElementTree as ET
import requests

def parse_and_organize_roll(xml_url):
    print(f"[*] Fetching and parsing XML from: {xml_url}")
    try:
        response = requests.get(xml_url, timeout=60)
        if response.status_code != 200:
            print(f"[-] Failed to fetch XML (Status: {response.status_code})")
            return
        
        root = ET.fromstring(response.content)
        records = []
        
        # Iterate through property/evaluation nodes
        for elem in root.iter():
            tags = {child.tag: child.text.strip() if child.text else "" for child in elem}
            if "RL0404A" in tags or "RL0402A" in tags:
                records.append({
                    "matricule": tags.get("RL0101", "N/A"),
                    "civic_number": tags.get("RL0105A", "N/A"),
                    "street": tags.get("RL0107A", "N/A"),
                    "land_value": tags.get("RL0402A", "0"),
                    "building_value": tags.get("RL0403A", "0"),
                    "total_value": tags.get("RL0404A", "0"),
                    "year_built": tags.get("RL0307A", "N/A"),
                    "use_code": tags.get("RL0307B", "N/A")
                })
                
        print(f"[+] Extracted and organized {len(records)} property records.")
        
        # Print sample records
        for r in records[:5]:
            print(f"  - [{r['matricule']}] Civic: {r['civic_number']} | Total Value: ${r['total_value']} | Built: {r['year_built']}")
            
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    rimouski_url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    parse_and_organize_roll(rimouski_url)
