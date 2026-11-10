import requests
import xml.etree.ElementTree as ET

def find_property_container():
    url = "https://donneesouvertes.affmunqc.net/role/RL10043_2026.xml"
    print("[*] Downloading and analyzing XML schema hierarchy...")
    res = requests.get(url, timeout=90)
    if res.status_code != 200:
        print("[-] Download failed.")
        return

    root = ET.fromstring(res.content)
    print(f"[+] Root tag: <{root.tag}>")
    
    # List distinct direct child tags of root
    root_children = set(child.tag for child in root)
    print(f"[*] Top-level container tags under root: {root_children}")

    # Locate the container element that holds RL0101x (address block)
    target_container = None
    for parent in root.iter():
        for child in parent:
            if child.tag == "RL0101x":
                # Check if civic 560 is in this RL0101x block
                block_data = {c.tag: c.text.strip() for c in child if c.text}
                if block_data.get("RL0101Ax") == "560":
                    target_container = parent
                    print(f"\n[+] Found Parent Container <{parent.tag}> for Civic 560:")
                    print(f"    Parent has {len(list(parent))} direct child tags: {[c.tag for c in parent]}")
                    
                    # Print all key-value pairs stored within this container
                    unit_tags = {}
                    for elem in parent.iter():
                        if elem.tag and elem.text and elem.text.strip():
                            unit_tags[elem.tag] = elem.text.strip()
                    
                    print("\n  [Aggregated Container Attributes]:")
                    for k, v in unit_tags.items():
                        print(f"    {k}: {v}")
                    return

if __name__ == "__main__":
    find_property_container()
