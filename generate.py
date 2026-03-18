import time
import random
import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://jp.mercari.com/search?keyword=初音ミク フィギュア"
AFF_LINK = "https://your-affiliate-link.com"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# ページ取得
res = requests.get(SEARCH_URL, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

imgs = soup.find_all("img")

thumbs = []

for img in imgs:
    src = img.get("src")
    
    if src and "static.mercdn.net" in src:
        thumbs.append(src)

# 重複削除
thumbs = list(set(thumbs))

# ランダム
random.shuffle(thumbs)

# 最大20件
thumbs = thumbs[:20]

# HTML生成
html = f'<a href="{AFF_LINK}">\n'

for img in thumbs:
    html += f'<img src="{img}" width="200">\n'

html += "</a>"

# 保存
with open("mercari.html","w",encoding="utf-8") as f:
    f.write(html)

print("生成完了")
