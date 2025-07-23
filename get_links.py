# Claude 4 rewrite 後沒跑過
import requests
from bs4 import BeautifulSoup
import time
import json
import urllib3
import random
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_valid_links(soup):
    """從網頁中提取有效的查核報告連結"""
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
    """爬取所有查核報告連結"""
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
        time.sleep(random.randint(1, 6))

    return list(all_links)

def classify_urls(urls):
    """將 URL 分類為 migration 和其他類別"""
    migration_urls = []
    other_urls = []

    for url in urls:
        if "migration" in url.lower():
            migration_urls.append(url)
        else:
            other_urls.append(url)
    
    return migration_urls, other_urls

def create_directories():
    """建立必要的目錄結構"""
    directories = ["data", "data/url"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 建立目錄: {directory}")

def save_json_file(data, filepath, description):
    """儲存 JSON 檔案"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 {description}: {len(data)} 筆資料儲存至 {filepath}")

if __name__ == "__main__":
    print("🚀 開始執行 TFC 查核報告爬蟲與分類程式")
    print("=" * 50)
    
    # 步驟 1: 建立目錄
    create_directories()
    
    # 步驟 2: 爬取所有連結
    print("\n📡 開始爬取查核報告連結...")
    report_links = crawl_links()
    
    # 步驟 3: 儲存所有連結
    all_links_file = "data/url/TFC_factcheck_links.json"
    save_json_file(report_links, all_links_file, "所有查核報告連結")
    
    # 步驟 4: 分類連結
    print("\n🔍 開始分類連結...")
    migration_urls, other_urls = classify_urls(report_links)
    
    # 步驟 5: 儲存分類結果
    migration_file = "data/url/migration.json"
    other_file = "data/url/title.json"
    
    save_json_file(migration_urls, migration_file, "Migration 相關連結")
    save_json_file(other_urls, other_file, "其他連結")
    
    print("\n" + "=" * 50)
    print("✅ 程式執行完成！")
    print(f"📊 總共處理 {len(report_links)} 筆連結")
    print(f"   - Migration 相關: {len(migration_urls)} 筆")
    print(f"   - 其他類別: {len(other_urls)} 筆")