import json

def generate_registre_foncier_query():
    district = "Rimouski"
    lot_number = "6336030"

    print(f"[*] Formatting Registre foncier du Québec request for Lot {lot_number}...")
    
    payload = {
        "service": "Registre foncier du Québec en ligne",
        "circonscription_fonciere": district,
        "mode_de_recherche": "INDEX_DES_IMMEUBLES",
        "cadastre": "Cadastre du Québec",
        "numero_lot": int(lot_number),
        "formatted_lot": f"{lot_number}",
        "documents_a_extraire": [
            "Index des immeubles",
            "Acte de vente (2020-09-30)",
            "Avis d'hypothèque",
            "Bordereau d'immatriculation"
        ]
    }

    print("\n[+] Formatted Query Payload:")
    print("=======================================================")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    generate_registre_foncier_query()
