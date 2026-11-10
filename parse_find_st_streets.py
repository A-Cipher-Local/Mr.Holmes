import requests
import xml.etree.ElementTree as ET
from collections import defaultdict

def scan_saint_streets():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print("[*] Downloading and scanning all street names in Rimouski roll...")
    res = requests.get(url, timeout=90)
    root = ET.fromstring(res.content)
    units = root.findall(".//RLUEx")

    streets = defaultdict(list)

    for u in units:
        unit_map = {n.tag: n.text.strip() for n in u.iter() if n.text and n.text.strip()}
        st_name = unit_map.get("RL0101Gx", "").upper()
        civic = unit_map.get("RL0101Ax", "")

        # Look for any variation of Saint / St / Louis
        if any(k in st_name for k in ["ST", "SAINT", "LOUIS"]):
            full_st = f"{unit_map.get('RL0101Ex', '')} {unit_map.get('RL0101Fx', '')} {st_name} {unit_map.get('RL0101Hx', '')}".strip()
            if civic.isdigit():
                streets[full_st].append(int(civic))

    print(f"\n[+] Unique 'SAINT / ST / LOUIS' streets found in Rimouski roll:")
    print("=" * 65)
    for st, civics in sorted(streets.items()):
        civics.sort()
        print(f"  - {st:<35} | Count: {len(civics):<4} | Range: {civics[0]} to {civics[-1]}")

if __name__ == "__main__":
    scan_saint_streets()
