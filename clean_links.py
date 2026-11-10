import re
import glob

def extract_clean_urls(input_pattern, output_file):
    urls = set()
    url_pattern = re.compile(r'https?://[^\s\|]+')
    
    for filepath in glob.glob(input_pattern):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                matches = url_pattern.findall(line)
                for match in matches:
                    urls.add(match)

    with open(output_file, 'w', encoding='utf-8') as f:
        for url in sorted(urls):
            f.write(url + '\n')

    print(f"[+] Cleaned and extracted {len(urls)} unique URLs to {output_file}.")

if __name__ == "__main__":
    extract_clean_urls("GUI/Reports/People/Dorks/*.txt", "extracted_dorks.txt")
