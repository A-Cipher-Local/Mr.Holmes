#!/usr/bin/env python3
import sys
from playwright.sync_api import sync_playwright

def search_req(address):
    print(f"[*] Launching browser context for: {address}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        url = "https://www.registreentreprises.gouv.qc.ca/RQPortal/fr/Direct/Recherche"
        print(f"[+] Accessing REQ portal: {url}...")
        page.goto(url, wait_until="domcontentloaded")

        # Wait for potential session redirect/cookies
        page.wait_for_timeout(2000)
        print(f"[*] Current Page Title: {page.title()}")
        print(f"[*] Target URL: {page.url}")
        
        browser.close()

if __name__ == "__main__":
    search_req("560 rue Saint-Louis-Ouest")
