import csv
import time
from bs4 import BeautifulSoup
import requests

def validate_and_scrape(input_file="extracted_dorks.txt", output_csv="validated_dorks_report.csv"):
    try:
        with open(input_file, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Error: {input_file} not found. Run your extraction step first.")
        return

    print(f"[*] Starting validation and scraping for {len(urls)} URLs...\n")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    results = []

    for idx, url in enumerate(urls, 1):
        print(f"[{idx}/{len(urls)}] Checking: {url}")
        
        status = "ERROR"
        title = "N/A"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            status = response.status_code
            
            if status == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                if soup.title and soup.title.string:
                    title = soup.title.string.strip().replace("\n", " ")
        except requests.exceptions.Timeout:
            status = "TIMEOUT"
        except requests.exceptions.ConnectionError:
            status = "CONN_ERROR"
        except Exception as e:
            status = f"FAILED: {type(e).__name__}"

        results.append({
            "URL": url,
            "Status": status,
            "Page Title": title
        })

        time.sleep(1.5)

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["URL", "Status", "Page Title"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"\n[+] Validation complete! Results saved to {output_csv}")

if __name__ == "__main__":
    validate_and_scrape()
