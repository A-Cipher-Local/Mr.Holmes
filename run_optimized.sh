#!/usr/bin/env bash
# Mr.Holmes Optimization & Safe Launcher Script

echo "[+] Starting Mr.Holmes optimization sequence..."

# 1. Clean up stale Python bytecode and cache folders to prevent weird runtime errors
echo "[*] Cleaning Python cache files..."
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# 2. Automatically activate virtual environment if present
if [ -d "venv" ] && [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "[*] Activating virtual environment (venv)..."
    source venv/bin/activate
fi

# 3. Quickly verify and update requirements if a requirements file exists
if [ -f "requirements.txt" ]; then
    echo "[*] Checking Python dependencies..."
    pip install --upgrade -q -r requirements.txt
fi

echo "[+] Environment preparation complete."
