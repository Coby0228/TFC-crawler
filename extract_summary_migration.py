import json
import requests
import time
import random
from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib3
import re

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_claim_from_title(soup):
    """從 HTML <title> 擷取 claim，去掉前綴符號與空格"""
    title_tag = soup.title
    if not title_tag or not title_tag.string:
        return None

    title_text = title_tag.string.strip()

    # 使用正則處理格式
    if '】' in title_text:
        pattern = r'】([^ ]+)'  # 】 後到第一個空白
    else:
        pattern = r'^([^ ]+)'  # 從開頭到第一個空白

    match = re.search(pattern, title_text)
    return match.group(1).strip() if match else title_text

def extract_type_from_title(soup):
    """從 HTML <title> 擷取 type，即【...】中的文字"""
    title_tag = soup.title
    if not title_tag or not title_tag.string:
        return None
    title_text = title_tag.string.strip()
    match = re.search(r'【(.*?)】', title_text)
    return match.group(1).strip() if match else None

def extract_fact_check_blocks(soup):
    """
    從 HTML 提取查核報告正文，並將所有段落合併為單一字串。
    此函式首先定位到 id 為 'kanban' 的 div 元素，然後尋找其後緊鄰的兄弟 div 元素，
    這個兄弟元素包含了所需的查核報告內容。
    """
    # 尋找 id="kanban" 的 div
    kanban_div = soup.find("div", id="kanban")
    
    if kanban_div:
        report_div = kanban_div.find_next_sibling("div")
        if report_div:
            paragraphs = report_div.find_all("p")
            report_texts = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
            return "\n".join(report_texts)

    return None

# 讀取網址清單
with open("data/url/migration.json", "r", encoding="utf-8") as f:
    urls = json.load(f)

results = []

for url in tqdm(urls, desc="抓取進度"):
    try:
        res = requests.get(url, verify=False, timeout=20)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        claim_text = extract_claim_from_title(soup)
        type_text = extract_type_from_title(soup)
        report_text = extract_fact_check_blocks(soup)

        result_entry = {
            "url": url,
            "claim": claim_text,
            "report": report_text,
            "type": type_text,
        }
        results.append(result_entry)

        # print(f"url: {url}")
        # print(f"claim: {claim_text}")
        # print(f"type: {type_text}")
        # print(f"report:\n{report_text}\n{'-'*50}")

        time.sleep(random.uniform(1, 6))

    except Exception as e:
        print(f"❌ 錯誤: {url} → {e}")
        results.append({"url": url, "error": str(e)})

# 儲存結果
with open("data/raw/TFC_migration_data.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("✅ 所有頁面已處理完畢")
