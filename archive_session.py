import os
import tarfile
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
archive_name = f"recon_archive_{timestamp}.tar.gz"

files_to_archive = [
    "brand_dork_results.json",
    "unique_urls.txt",
    "unique_domains.txt",
    "extracted_dorks.txt"
]

print(f"[*] Creating compressed archive: {archive_name}")
with tarfile.open(archive_name, "w:gz") as tar:
    for filename in files_to_archive:
        if os.path.exists(filename):
            tar.add(filename)
            print(f"  [+] Added: {filename}")
            
    if os.path.exists("intel_cache"):
        tar.add("intel_cache")
        print("  [+] Added: intel_cache/")

print(f"\n[+] Archive successfully created and secured as {archive_name}")
