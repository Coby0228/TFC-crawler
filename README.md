## uv 建立環境 (Windows)
```powershell
uv init
uv add tqdm requests beautifulsoup4
```

發佈日期：2024-11-28 前為 migration，之後為 title

- [migration](https://tfc-taiwan.org.tw/fact-check-reports/migration-106/)
- [title](https://tfc-taiwan.org.tw/fact-check-reports/us-taiwan-trade-32-percent-tariff-not-final/)

1. get_links: 取得要爬取的所有連結
2. urls_classification: 根據格式不同分類
3. extract_summary_title: 取得 title 類別中的網站內文摘要
