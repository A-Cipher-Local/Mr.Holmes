#!/usr/bin/env python3
import os

proxy_file_path = "Core/Support/Proxies.py"

if not os.path.exists(proxy_file_path):
    print("[-] Error: Core/Support/Proxies.py not found.")
    exit(1)

print("[*] Backing up Proxies.py...")
with open(proxy_file_path, "r") as f:
    code = f.read()

with open(proxy_file_path + ".bak", "w") as f:
    f.write(code)

# Patch the file opening logic to check if Proxy_file exists and is not 'None'
old_snippet = """    f = open(Proxy_file, "r")"""
new_snippet = """    if Proxy_file and Proxy_file.lower() != "none" and os.path.exists(Proxy_file):
        f = open(Proxy_file, "r")
    else:
        f = []"""

if old_snippet in code:
    code = code.replace(old_snippet, new_snippet)
    with open(proxy_file_path, "w") as f:
        f.write(code)
    print("[+] Successfully patched Core/Support/Proxies.py to handle missing or 'None' proxy lists gracefully!")
else:
    print("[!] Target pattern not found. Let's inspect or apply manual fix.")
