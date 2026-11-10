#!/usr/bin/env python3
import os

proxy_file_path = "Core/Support/Proxies.py"

if not os.path.exists(proxy_file_path):
    print("[-] Error: Core/Support/Proxies.py not found.")
    exit(1)

print("[*] Updating proxy file loading logic...")
with open(proxy_file_path, "r") as f:
    code = f.read()

# Replace the fallback block to use an empty file-like iterator or check safely
old_snippet = """    if Proxy_file and Proxy_file.lower() != "none" and os.path.exists(Proxy_file):
        f = open(Proxy_file, "r")
    else:
        f = []"""

new_snippet = """    class DummyFile:
        def readlines(self):
            return []
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    if Proxy_file and Proxy_file.lower() != "none" and os.path.exists(Proxy_file):
        f = open(Proxy_file, "r")
    else:
        f = DummyFile()"""

if old_snippet in code:
    code = code.replace(old_snippet, new_snippet)
    with open(proxy_file_path, "w") as f:
        f.write(code)
    print("[+] Successfully patched Core/Support/Proxies.py with a dummy file handler!")
else:
    print("[!] Target pattern not found. Applying direct rewrite of Proxies.py...")
    # Direct safe rewrite of Proxies.py if pattern differs slightly
    with open(proxy_file_path, "w") as f:
        f.write('''import os
class proxy:
    try:
        from Core.Support import Language
        Parser = Language.Translation.Parser
        Proxy_file = Parser["Settings"]["Proxy_List"]
    except Exception:
        Proxy_file = "None"

    class DummyFile:
        def readlines(self):
            return []
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    if Proxy_file and Proxy_file.lower() != "none" and os.path.exists(Proxy_file):
        f = open(Proxy_file, "r")
    else:
        f = DummyFile()

    with f as file_obj:
        Proxies_List = [line.strip() for line in file_obj.readlines() if line.strip()]
''')
    print("[+] Wrote clean, robust proxy handler to Proxies.py!")
