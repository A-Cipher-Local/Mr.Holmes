import requests
import xml.etree.ElementTree as ET
import io

def find_all_560(xml_url):
    print(f"[*] Downloading and scanning XML for '560'...")
    res = requests.get(xml_url, timeout=90)
    if res.status_code != 200:
        print("[-] Download failed.")
        return

    root = ET.fromstring(res.content)
    matches = 0

    # Search every element and its children for the number 560
    for parent in root.iter():
        # Check if any child text equals 560
        has_560 = False
        unit_data = {}
        for child in parent:
            val = child.text.strip() if child.text else ""
            unit_data[child.tag] = val
            if val == "560":
                has_560 = True

        if has_560:
            matches += 1
            print(f"\n[+] Found Target Text Match #{matches} (Parent Tag: {parent.tag}):")
            for k, v in unit_data.items():
                if v:
                    print(f"    {k}: {v}")

    print(f"\n[*] Total elements matching '560': {matches}")

if __name__ == "__main__":
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    find_all_560(url)
