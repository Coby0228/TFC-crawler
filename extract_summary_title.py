from bs4 import BeautifulSoup

# 讀取 HTML 檔案
with open("林蛙確實能在結凍後復甦，但網傳圖片並非阿拉斯加林蛙 - 看見真實，才能打造美好台灣.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 找出所有 class 包含 'has-theme-palette-7-background-color' 的 <p> 標籤
paragraphs = soup.find_all("p", class_=lambda x: x and 'has-theme-palette-7-background-color' in x)

# 印出所有符合條件的文字段落
for idx, p in enumerate(paragraphs, 1):
    print(f"[段落 {idx}]")
    print(p.get_text(strip=True))
    print("-" * 40)
