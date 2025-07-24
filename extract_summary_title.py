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

for url in tqdm(urls[:3], desc="抓取進度"):
    res = requests.get(url, verify=False, timeout=20)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    # 擷取 claim
    claim_tag = soup.select_one("p.wp-block-kadence-advancedheading")
    claim_text = claim_tag.get_text(strip=True) if claim_tag else None

    # 擷取段落內容
    paragraphs = soup.find_all("p", class_=lambda x: x and "has-theme-palette-7-background-color" in x)

    # verdict_description 取第一段
    verdict_description = paragraphs[0].get_text(strip=True) if len(paragraphs) > 0 else None

    # report 取第二段之後合併
    report = "\n".join([p.get_text(strip=True) for p in paragraphs[1:]]) if len(paragraphs) > 1 else None

    # 組裝結果
    result_entry = {
        "url": url,
        "claim": claim_text,
        "verdict_description": verdict_description,
        "report": report
    }

    results.append(result_entry)

    # 隨機 sleep，防止封鎖
    time.sleep(random.uniform(1, 6))

# 儲存結果
with open("data/raw/TFC_title_data.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("✅ 所有頁面已處理完畢")
