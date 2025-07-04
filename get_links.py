import requests
from bs4 import BeautifulSoup
import time
import json
import urllib3
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_valid_links(soup):
    raw_links = soup.select("div.entry-content-wrap a")
    valid_links = []

    for a in raw_links:
        href = a.get("href")
        if href and "/fact-check-reports/" in href and not (
            "report-type" in href or "report-classification" in href
        ):
            valid_links.append(href)

    return valid_links

def crawl_links():
    base_url = "https://tfc-taiwan.org.tw/fact-check-reports-all/?pg={}"
    page = 1
    all_links = set()

    while True:
        url = base_url.format(page)
        print(f"📄 抓取第 {page} 頁: {url}")
        try:
            res = requests.get(url, verify=False, timeout=10)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ 錯誤，第 {page} 頁無法抓取：{e}")
            break

        soup = BeautifulSoup(res.text, "html.parser")
        links = extract_valid_links(soup)

        if not links:
            print("✅ 沒有更多資料，結束翻頁。")
            break

        all_links.update(links)
        page += 1
        time.sleep(random.randint(1,6))

    return list(all_links)

# 執行爬蟲
report_links = crawl_links()

# 存成 JSON
with open("TFC_factcheck_links.json", "w", encoding="utf-8") as f:
    json.dump(report_links, f, ensure_ascii=False, indent=4)

print(f"✅ 共儲存 {len(report_links)} 筆查核報告連結到 factcheck_links.json")
