#!/usr/bin/env python3
import urllib.request

def dump_file(repo, filepath):
    url = f"https://raw.githubusercontent.com/{repo}/main/{filepath}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode("utf-8")
    except:
        url_master = f"https://raw.githubusercontent.com/{repo}/master/{filepath}"
        req = urllib.request.Request(url_master, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode("utf-8")

if __name__ == "__main__":
    repo = "HappyPunch/hp-reports"
    filepath = "source/server.lua"
    print(f"[*] Dumping full content of {filepath} from {repo}:\n")
    content = dump_file(repo, filepath)
    print(content)
