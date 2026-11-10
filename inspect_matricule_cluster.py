import xml.etree.ElementTree as ET

def find_matricule_cluster():
    tree = ET.parse('RL10043_2026.xml')
    print("[*] Searching for evaluation units sharing Matricule components with Lot 6336030 (2567-92-8197)...")
    
    matches = []
    for u in tree.findall('.//RLUEx'):
        a = u.findtext('.//RL0104A', '')
        b = u.findtext('.//RL0104B', '')
        c = u.findtext('.//RL0104C', '')
        lot = u.findtext('.//RL0103Ax', '')
        civic = u.findtext('.//RL0101Ax', '')
        street = u.findtext('.//RL0101Gx', '')
        total_val = u.findtext('.//RL0404A', '0')
        units = u.findtext('.//RL0502A', '1')
        
        # Check if it matches any part of the target matricule
        if a == '2567' or (a == '2567' and b == '92'):
            matches.append({
                "lot": lot,
                "civic": civic,
                "street": street,
                "matricule": f"{a}-{b}-{c}",
                "units": units,
                "total_val": total_val
            })

    print(f"\n[+] Found {len(matches)} units matching matricule family 2567:")
    print("=" * 80)
    for m in matches:
        marker = " <=== [TARGET LOT 6336030]" if m['lot'] == '6336030' else ""
        print(f"Lot: {m['lot']:<8} | Civic: {m['civic']:<4} {m['street']:<16} | Mat: {m['matricule']} | Units: {m['units']:<2} | Val: ${m['total_val']}{marker}")

if __name__ == "__main__":
    find_matricule_cluster()
