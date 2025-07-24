# [Taiwan FactCheck Center](https://tfc-taiwan.org.tw/)

## uv 建立環境 (Windows)

```powershell
uv init
uv add tqdm requests beautifulsoup4
```

## 格式差異

網站在 2024-11-28 進行了**網站結構改版**，因此查核報告的 URL 與 HTML 結構分成兩種格式：

- 2024-11-28 之前 → 使用 migration 格式

- 2024-11-28 之後 → 使用 title 格式

範例：
- [migration](https://tfc-taiwan.org.tw/fact-check-reports/migration-106/)
- [title](https://tfc-taiwan.org.tw/fact-check-reports/us-taiwan-trade-32-percent-tariff-not-final/)

## 使用方法

- get_links: 取得查核報告的所有連結
- extract_summary_title: 取得 title 格式的**內文摘要**，回傳 Json 結構如下
  - url
  - claim
  - verdict_description
  - report
- extract_summary_migration: 取得 migration 格式的**查核報告**及**判決結果**，回傳 Json 結構如下
  - url
  - claim
  - report
  - verdict
