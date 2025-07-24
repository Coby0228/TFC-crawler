import json
import requests
import time
import random
from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib3
import re
import os

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Checkpoint 設定
CHECKPOINT_FILE = "data/checkpoint/scraper_checkpoint.json"
OUTPUT_FILE = "data/raw/TFC_migration_data.json"
CHECKPOINT_INTERVAL = 500  # 每處理 500 個網址就儲存一次 checkpoint

def load_checkpoint():
    """載入 checkpoint 檔案"""
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                checkpoint = json.load(f)
            print(f"📁 載入 checkpoint: 已完成 {checkpoint['completed_count']} 個網址")
            return checkpoint
        except Exception as e:
            print(f"⚠️ 載入 checkpoint 失敗: {e}")
    return {"completed_urls": [], "results": [], "completed_count": 0}

def save_checkpoint(checkpoint):
    """儲存 checkpoint 檔案"""
    try:
        # 確保目錄存在
        os.makedirs(os.path.dirname(CHECKPOINT_FILE), exist_ok=True)
        
        with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ 儲存 checkpoint 失敗: {e}")

def save_final_results(results):
    """儲存最終結果"""
    try:
        # 確保目錄存在
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"💾 結果已儲存到: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ 儲存結果失敗: {e}")

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

def main():
    # 讀取網址清單
    try:
        with open("data/url/migration.json", "r", encoding="utf-8") as f:
            urls = json.load(f)
    except FileNotFoundError:
        print("❌ 找不到網址檔案: data/url/migration.json")
        return
    except Exception as e:
        print(f"❌ 讀取網址檔案失敗: {e}")
        return

    # 載入 checkpoint
    checkpoint = load_checkpoint()
    completed_urls = set(checkpoint["completed_urls"])
    results = checkpoint["results"]
    
    # 過濾出尚未處理的網址
    remaining_urls = [url for url in urls if url not in completed_urls]
    
    if not remaining_urls:
        print("🎉 所有網址都已處理完畢！")
        return
    
    print(f"📊 總共 {len(urls)} 個網址，已完成 {len(completed_urls)} 個，剩餘 {len(remaining_urls)} 個")

    # 開始處理剩餘的網址
    for i, url in enumerate(tqdm(remaining_urls, desc="抓取進度")):
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
            completed_urls.add(url)

            # 每隔一定間隔儲存 checkpoint
            if (i + 1) % CHECKPOINT_INTERVAL == 0:
                checkpoint_data = {
                    "completed_urls": list(completed_urls),
                    "results": results,
                    "completed_count": len(completed_urls)
                }
                save_checkpoint(checkpoint_data)
                print(f"💾 Checkpoint 已儲存 ({len(completed_urls)}/{len(urls)})")

            time.sleep(random.uniform(1, 6))

        except Exception as e:
            print(f"❌ 錯誤: {url} → {e}")
            error_entry = {"url": url, "error": str(e)}
            results.append(error_entry)
            completed_urls.add(url)  # 即使出錯也標記為已處理，避免重複嘗試

    # 最終儲存
    final_checkpoint = {
        "completed_urls": list(completed_urls),
        "results": results,
        "completed_count": len(completed_urls)
    }
    save_checkpoint(final_checkpoint)
    save_final_results(results)

    print("✅ 所有頁面已處理完畢")

if __name__ == "__main__":
    main()