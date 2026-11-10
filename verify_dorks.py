import csv
import time
import requests
from bs4 import BeautifulSoup

def verify_dork_endpoints(input_file="extracted_dorks.txt", output_csv="verified_dorks.csv"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    verified_data = []

    try:
        with open(input_file, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Error: {input_file} not found.")
        return

    for idx, url in enumerate(urls, 1):
        print(f"[{idx}/{len(urls)}] Checking: {url}")
        
        try:
            res = requests.get(url, headers=headers, timeout=10)
            status = res.status_code

            if status == 429:
                print("    [-] Rate limited (429). Pausing for 10 seconds...")
                time.sleep(10)
                continue

            soup = BeautifulSoup(res.text, "html.parser")
            page_title = soup.title.string.strip() if soup.title and soup.title.string else "N/A"

            if "sorry" in page_title.lower() or "captcha" in page_title.lower():
                status = "BLOCKED_CAPTCHA"

            verified_data.append({
                "URL": url,
                "Status": status,
                "Title": page_title
            })

        except Exception as e:
            verified_data.append({"URL": url, "Status": "FAILED", "Title": str(e)})

        time.sleep(4)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["URL", "Status", "Title"])
        writer.writeheader()
        writer.writerows(verified_data)

    print(f"\n[+] Processing complete. Saved to {output_csv}")

if __name__ == "__main__":
    verify_dork_endpoints()
