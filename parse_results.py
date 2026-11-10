import json

with open("brand_dork_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for target, queries in data.items():
    print(f"\n=== TARGET: {target} ===")
    for q, results in queries.items():
        print(f"  [Query: {q}] -> {len(results)} hits")
        for r in results:
            print(f"    - {r.get('href')} ({r.get('title')})")
