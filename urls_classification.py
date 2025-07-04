import json

with open("data/TFC_factcheck_links.json", "r", encoding="utf-8") as f:
    urls = json.load(f)

migration_urls = []
other_urls = []

for url in urls:
    if "migration" in url.lower():
        migration_urls.append(url)
    else:
        other_urls.append(url)

with open("data/migration.json", "w", encoding="utf-8") as f:
    json.dump(migration_urls, f, ensure_ascii=False, indent=2)

with open("data/title.json", "w", encoding="utf-8") as f:
    json.dump(other_urls, f, ensure_ascii=False, indent=2)

print("分類完成！")
