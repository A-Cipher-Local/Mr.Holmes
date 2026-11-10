#!/usr/bin/env bash
TARGET_FILE="Core/Searcher_person.py"

echo "[+] Checking for $TARGET_FILE..."

if [ ! -f "$TARGET_FILE" ]; then
    echo "[-] Error: $TARGET_FILE not found. Are you in the Mr.Holmes root directory?"
    exit 1
fi

echo "[*] Creating backup of original Searcher_person.py as Searcher_person.py.bak..."
cp "$TARGET_FILE" "${TARGET_FILE}.bak"

echo "[*] Patching os.mkdir to os.makedirs with exist_ok=True..."

python3 -c '
path = "Core/Searcher_person.py"
with open(path, "r") as f:
    code = f.read()

# Replace unsafe os.mkdir calls for folder creation with exist_ok=True
old_pattern = "os.mkdir(folder)"
new_pattern = "os.makedirs(folder, exist_ok=True)"

if old_pattern in code:
    code = code.replace(old_pattern, new_pattern)
    with open(path, "w") as f:
        f.write(code)
    print("[+] Successfully patched os.mkdir to os.makedirs.")
else:
    print("[!] Target pattern os.mkdir(folder) not found or already patched.")
'

echo "[+] Fix complete! You can now run Mr.Holmes again."
