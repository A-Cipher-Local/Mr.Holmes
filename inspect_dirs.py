import os

reports_dir = "GUI/Reports"
print("[*] Inspecting contents of category directories inside GUI/Reports/...\n")

categories = ["Usernames", "Websites", "E-Mail", "Phone", "People", "Dorks", "Ports"]

for cat in categories:
    cat_path = os.path.join(reports_dir, cat)
    if os.path.isdir(cat_path):
        files = os.listdir(cat_path)
        print(f"[{cat}/] -> Contains {len(files)} files: {files}")
        for f in files:
            f_path = os.path.join(cat_path, f)
            if os.path.isfile(f_path) and os.path.getsize(f_path) > 0:
                try:
                    with open(f_path, "r", encoding="utf-8", errors="ignore") as sub_f:
                        preview = sub_f.read().strip()
                        print(f"    - {f} ({os.path.getsize(f_path)} bytes): {preview[:100]}")
                except Exception as e:
                    print(f"    - {f}: Error reading -> {e}")
    else:
        print(f"[{cat}] -> Not a directory or does not exist.")
