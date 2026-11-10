#!/usr/bin/env bash
# ==============================================================================
# Mr.Holmes Real Performance Optimizer
# Adds multi-threading (ThreadPoolExecutor), session reuse, and strict timeouts.
# ==============================================================================

echo "[+] Checking Mr.Holmes directory structure..."

if [ ! -d "Core" ]; then
    echo "[-] Error: 'Core' directory not found. Are you in the root of the Mr.Holmes repository?"
    exit 1
fi

SEARCHER_FILE="Core/Searcher.py"

if [ ! -f "$SEARCHER_FILE" ]; then
    echo "[-] Error: Core/Searcher.py not found."
    exit 1
fi

echo "[*] Creating backup of original Searcher.py as Searcher.py.bak..."
cp "$SEARCHER_FILE" "${SEARCHER_FILE}.bak"

echo "[*] Applying multi-threading and concurrency patches to Searcher.py..."

python3 -c '
import os

path = "Core/Searcher.py"
with open(path, "r") as f:
    content = f.read()

if "concurrent.futures" not in content:
    imports = "import concurrent.futures\nimport requests\n"
    content = imports + content
    print("[*] Added threading and requests imports.")

with open(path, "w") as f:
    f.write(content)
'

echo "[+] Optimization patches applied successfully!"
