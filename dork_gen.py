#!/usr/bin/env python3

TARGET_ALIASES = ["Tammy Busagi", "DemonSmooch", "smooch"]
TARGET_PLATFORMS = ["hikkipedia.com", "youtube.com", "twitch.tv", "pastebin.com", "github.com", "archive.org"]

def generate_dorks():
    for alias in TARGET_ALIASES:
        print(f"=== Target: {alias} ===")
        for platform in TARGET_PLATFORMS:
            print(f"site:{platform} \"{alias}\"")
        print(f"\"index of/\" \"{alias}\"")
        print(f"\"{alias}\" ext:txt OR ext:log OR ext:json")
        print("-" * 40)

if __name__ == "__main__":
    generate_dorks()
