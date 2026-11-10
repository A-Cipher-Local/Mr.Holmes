import os
import re

print("[*] Executing deep regex sweep for endpoints, IPs, and hidden strings...\n")

patterns = {
    "IP Address": re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'),
    "API / URL Endpoint": re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+'),
    "Token / Secret Keyword": re.compile(r'(token|secret|key|auth|password|webhook)', re.IGNORECASE)
}

for root, dirs, files in os.walk("."):
    if "venv" in root or ".git" in root:
        continue
    for file in files:
        if file.endswith((".lua", ".json", ".txt")):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for line_no, line in enumerate(f, 1):
                        for label, pattern in patterns.items():
                            if pattern.search(line):
                                print(f"[{file}:{line_no}] ({label}) -> {line.strip()}")
            except Exception:
                pass
