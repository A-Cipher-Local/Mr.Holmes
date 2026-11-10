import requests
import xml.etree.ElementTree as ET
import csv

def analyze_saint_louis():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print("[*] Fetching Rimouski roll...")
    res = requests.get(url, timeout=90)
    if res.status_code != 200:
        print("[-] Download failed.")
        return

    root = ET.fromstring(res.content)
    units = root.findall(".//RLUEx")

    records = []
    for u in units:
        unit_map = {n.tag: n.text.strip() for n in u.iter() if n.text and n.text.strip()}
        street = unit_map.get("RL0101Gx", "").upper()
        
        if "LOUIS" in street:
            civic = unit_map.get("RL0101Ax", "")
            records.append({
                "civic": civic,
                "type": unit_map.get("RL0101Ex", ""),
                "orientation": unit_map.get("RL0101Hx", ""),  # E.g., 'O' for Ouest
                "street": street,
                "land_val": unit_map.get("RL0402A", "0"),
                "bldg_val": unit_map.get("RL0403A", "0"),
                "total_val": unit_map.get("RL0404A", "0"),
                "year_built": unit_map.get("RL0307A", "N/A"),
                "use_code": unit_map.get("RL0307B", "N/A"),
                "matricule": unit_map.get("RL0101", "N/A")
            })

    # Sort numerically by civic number
    valid_records = [r for r in records if r['civic'].isdigit()]
    valid_records.sort(key=lambda x: int(x['civic']))

    print(f"\n[+] Total properties on Saint-Louis: {len(records)}")
    print("\n--- Properties in the 500-600 Civic Range ---")
    
    nearby = [r for r in valid_records if 500 <= int(r['civic']) <= 600]
    if nearby:
        for r in nearby:
            print(f"  Civic {r['civic']} {r['type']} {r['street']} {r['orientation']} | Total: ${r['total_val']} | Built: {r['year_built']}")
    else:
        print("[-] No numeric civic numbers found between 500 and 600.")
        print("[*] Nearest lower/higher civics on Saint-Louis:")
        lowers = [r for r in valid_records if int(r['civic']) < 500]
        highers = [r for r in valid_records if int(r['civic']) > 600]
        if lowers:
            print(f"    Max below 500: Civic {lowers[-1]['civic']} {lowers[-1]['street']}")
        if highers:
            print(f"    Min above 600: Civic {highers[0]['civic']} {highers[0]['street']}")

    # Save all Saint-Louis records to CSV for quick local querying
    with open("saint_louis_properties.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print("\n[+] Full list saved to 'saint_louis_properties.csv'.")

if __name__ == "__main__":
    analyze_saint_louis()
