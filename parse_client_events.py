import re

print("[*] Parsing hp_client.lua for trigger events and network hooks:\n")
with open("intel_cache/hp_client.lua", "r", encoding="utf-8", errors="ignore") as f:
    for line_no, line in enumerate(f, 1):
        if "TriggerServerEvent" in line or "RegisterNetEvent" in line or "net: " in line.lower():
            print(f"  Line {line_no}: {line.strip()}")
