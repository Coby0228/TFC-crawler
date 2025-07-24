# [Taiwan FactCheck Center](https://tfc-taiwan.org.tw/)

## uv 建立環境 (Windows)

```powershell
uv init
uv add tqdm requests beautifulsoup4
```

## 格式

發佈日期：2024-11-28 前為 migration，之後為 title

範例：
- [migration](https://tfc-taiwan.org.tw/fact-check-reports/migration-106/)
- [title](https://tfc-taiwan.org.tw/fact-check-reports/us-taiwan-trade-32-percent-tariff-not-final/)

## 使用方法

- get_links: 取得查核報告的所有連結
- extract_summary_title: 取得 title 格式的內文摘要
- extract_summary_migration: 取得 migration 格式的查核報告
