import os
import json
import subprocess

REPORT_PATH = "GUI/Reports/deep_probe_report.json"
PROXY = "socks5h://127.0.0.1:9050"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def main():
    if not os.path.exists(REPORT_PATH):
        print(f"[-] Report not found at {REPORT_PATH}.")
        return

    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    dorks = data.get("cross_reference_dorks", [])
    print(f"[*] Loaded {len(dorks)} dork vectors from report.")
    print(f"[*] Routing requests through Tor proxy: {PROXY}\n")

    results = []
    for idx, url in enumerate(dorks, 1):
        print(f"[{idx}/{len(dorks)}] Testing vector...")
        cmd = [
            "curl", "--socks5-hostname", "127.0.0.1:9050",
            "-s", "-o", "/dev/null", "-w", "%{http_code}",
            "-A", USER_AGENT,
            "--max-time", "10",
            url
        ]
        
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=12)
            status = res.stdout.strip()
            print(f"    -> Status: {status} | {url[:60]}...")
            results.append({"url": url, "status": status})
        except Exception as e:
            print(f"    -> Error: {e}")
            results.append({"url": url, "status": "ERROR", "details": str(e)})

    out_log = "GUI/Reports/tor_dork_test_results.json"
    with open(out_log, "w", encoding="utf-8") as out:
        json.dump(results, out, indent=4)
    print(f"\n[+] Test complete. Results logged to {out_log}")

if __name__ == "__main__":
    main()
