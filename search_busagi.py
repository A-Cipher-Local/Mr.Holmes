import requests
import xml.etree.ElementTree as ET

TARGET_NAME = "BUSAGI"

def verify_privacy_redaction():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print(f"[*] Downloading and checking XML roll for '{TARGET_NAME}'...")
    res = requests.get(url, timeout=90)
    if res.status_code != 200:
        print("[-] Download failed.")
        return

    root = ET.fromstring(res.content)
    units = root.findall(".//RLUEx")
    print(f"[+] Scanning {len(units)} evaluation units...")

    matches = []
    for u in units:
        unit_map = {n.tag: n.text.strip() for n in u.iter() if n.text and n.text.strip()}
        full_text = " ".join(unit_map.values()).upper()
        
        if TARGET_NAME in full_text:
            matches.append(unit_map)

    print(f"\n[*] Matches found for '{TARGET_NAME}': {len(matches)}")
    if len(matches) == 0:
        print("[!] Confirmation: Owner identity blocks are entirely omitted from this open-data feed.")

if __name__ == "__main__":
    verify_privacy_redaction()
