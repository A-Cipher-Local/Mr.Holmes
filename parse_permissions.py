print("[*] Parsing hp_config.lua for permission tiers and admin identifiers:\n")
with open("intel_cache/hp_config.lua", "r", encoding="utf-8", errors="ignore") as f:
    for line_no, line in enumerate(f, 1):
        if any(kw in line.lower() for kw in ["group", "admin", "permission", "ace", "identifier"]):
            print(f"  Line {line_no}: {line.strip()}")
