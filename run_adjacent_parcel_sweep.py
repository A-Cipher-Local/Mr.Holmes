import requests
import xml.etree.ElementTree as ET

TARGET_LOT = "6336030"

def sweep_adjacent_parcels():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print(f"[*] Downloading evaluation roll to sweep adjacent parcels around Lot {TARGET_LOT}...")
    res = requests.get(url, timeout=90)
    if res.status_code != 200:
        print("[-] Download failed.")
        return

    root = ET.fromstring(res.content)
    units = root.findall(".//RLUEx")

    matches = []
    for u in units:
        unit_map = {n.tag: n.text.strip() for n in u.iter() if n.text and n.text.strip()}
        
        street = unit_map.get("RL0101Gx", "").upper()
        civic = unit_map.get("RL0101Ax", "")
        lot = unit_map.get("RL0103Ax", "N/A")

        if ("GERMAIN" in street or "LOUIS" in street) and civic.isdigit() and 540 <= int(civic) <= 580:
            matches.append({
                "civic": civic,
                "type": unit_map.get("RL0101Ex", ""),
                "street": f"{unit_map.get('RL0101Ex', '')} {street}",
                "lot": lot,
                "total_val": unit_map.get("RL0404A", "0"),
                "units": unit_map.get("RL0502A", "1"),
                "year": unit_map.get("RL0307A", "N/A")
            })

    matches.sort(key=lambda x: int(x['civic']) if x['civic'].isdigit() else 0)

    print(f"\n[+] Extracted {len(matches)} Contiguous Parcels at Sector Junction:")
    print("=" * 80)
    for m in matches:
        tag_marker = " <=== [TARGET LOT 6336030]" if m['lot'] == TARGET_LOT else ""
        print(f"Civic {m['civic']:<4} {m['street']:<22} | Lot: {m['lot']:<8} | Units: {m['units']:<2} | Total: ${m['total_val']}{tag_marker}")

if __name__ == "__main__":
    sweep_adjacent_parcels()
