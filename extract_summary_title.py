import json
import requests
import time
import random
from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 讀取網址清單
with open("data/url/title.json", "r", encoding="utf-8") as f:
    urls = json.load(f)

results = []

for url in tqdm(urls, desc="抓取進度"):
    try:
        res = requests.get(url, verify=False, timeout=10)
        res.raise_for_status()  # 如有錯會丟出 exception

        soup = BeautifulSoup(res.text, "html.parser")

        paragraphs = soup.find_all("p", class_=lambda x: x and "has-theme-palette-7-background-color" in x)
        text_blocks = [p.get_text(strip=True) for p in paragraphs]

        results.append({
            "url": url,
            "plaintext": "\n".join(text_blocks)
        })

    except Exception as e:
        print(f"❌ 錯誤: {url} → {e}")
        results.append({
            "url": url,
            "plaintext": None,
            "error": str(e)
        })

    # 隨機 sleep，防止封鎖
    time.sleep(random.uniform(1, 6))

# 儲存結果
with open("data/raw/title_summary.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ 所有頁面已處理完畢，結果儲存於 data/summary.json")
