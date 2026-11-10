#!/usr/bin/env bash
CONFIG_FILE="Configuration/Configuration.ini"
<<<<<<< HEAD
GITHUB_TOKEN="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"
=======
GITHUB_TOKEN="github_pat_11CFBJ6AQ0Bj9tWFPpSxSA_YOUR_TOKEN_HEREZgQWuZaIRCPMTAKhX39ZIOV"
>>>>>>> 39f90d6 (chore: sanitize hardcoded tokens and update core OSINT modules)

if [ -f "$CONFIG_FILE" ]; then
    if grep -q "api_key" "$CONFIG_FILE"; then
        sed -i "s/^api_key[[:space:]]*=.*/api_key = $GITHUB_TOKEN/" "$CONFIG_FILE"
        echo "[+] Updated existing api_key in $CONFIG_FILE"
    else
        echo "api_key = $GITHUB_TOKEN" >> "$CONFIG_FILE"
        echo "[+] Added api_key to $CONFIG_FILE"
    fi
else
    echo "[-] Error: $CONFIG_FILE not found. Make sure you are in the Mr.Holmes root directory."
fi
