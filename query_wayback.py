import os
import json
import subprocess

TARGET_DOMAIN = "stlawrenceparish"
CDX_URL = f"https://web.archive.org/cdx/search/cdx?url={TARGET_DOMAIN}*&output=json&limit=50"
PROXY = "socks5h://127.0.0.1:9050"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def main():
    print(f"[*] Querying Wayback Machine CDX API for target domain: {TARGET_DOMAIN}")
    print(f"[*] Routing via Tor proxy: {PROXY}")

    cmd = [
        "curl", "--socks5-hostname", "127.0.0.1:9050",
        "-s", "-A", USER_AGENT,
        "--max-time", "15",
        CDX_URL
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if res.returncode != 0:
            print(f"[-] Curl execution failed with return code {res.returncode}")
            return

        raw_output = res.stdout.strip()
        if not raw_output:
            print("[-] Received empty response from CDX API.")
            return

        data = json.loads(raw_output)
        print(f"[+] CDX API returned {len(data)} total records (including header).")

        os.makedirs("GUI/Reports", exist_ok=True)
        out_path = "GUI/Reports/wayback_stlawrenceparish.json"
        
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[+] Saved raw records to {out_path}")

        # Display first few captures if available
        if len(data) > 1:
            print("\n--- SAMPLE HISTORICAL SNAPSHOTS ---")
            header = data[0]
            for row in data[1:10]:
                timestamp = row[1] if len(row) > 1 else "N/A"
                original_url = row[2] if len(row) > 2 else "N/A"
                status = row[4] if len(row) > 4 else "N/A"
                print(f"  [{timestamp}] Status {status} -> {original_url}")
        else:
            print("[-] No historical captures found in CDX for this pattern.")

    except json.JSONDecodeError:
        print("[-] Error: Response was not valid JSON (possible proxy block or rate limit).")
        print(f"Response snippet: {raw_output[:200]}")
    except Exception as e:
        print(f"[-] Execution error: {e}")

if __name__ == "__main__":
    main()
