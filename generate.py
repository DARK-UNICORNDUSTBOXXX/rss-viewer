import feedparser
import random
import requests
from bs4 import BeautifulSoup

RSS_URL = "RSS_URL"
MERCARI_SEARCH = "https://jp.mercari.com/search?keyword=初音ミク フィギュア"

# RSS取得
feed = feedparser.parse(RSS_URL)

# メルカリ検索ページ取得
r = requests.get(MERCARI_SEARCH, headers={"User-Agent":"Mozilla/5.0"})
soup = BeautifulSoup(r.text,"html.parser")

mercari_items = []

for a in soup.select("a[href*='/item/']"):

    link = "https://jp.mercari.com" + a["href"]

    img = a.find("img")
    if not img:
        continue

    src = img.get("src") or img.get("data-src")
    if not src:
        continue

    mercari_items.append((link,src))

# ランダム6件
ads = random.sample(mercari_items, min(6,len(mercari_items)))

# RSS作成
rss_html = ""

for e in feed.entries[:30]:

    img = ""

    if "summary" in e:
        s = BeautifulSoup(e.summary,"html.parser")
        tag = s.find("img")
        if tag:
            img = tag.get("src") or tag.get("data-src") or ""

    rss_html += f"""
<div class="rss-item">
<a href="{e.link}" target="_blank">
<img src="{img}">
<div class="title">{e.title}</div>
</a>
</div>
"""

# 広告HTML
ads_html = '<a href="https://px.a8.net/svt/ejp?a8mat=XXXX">\n'

for link,img in ads:
    ads_html += f'<img src="{img}" class="adimg">\n'

ads_html += "</a>"

# HTML生成
html = f"""
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="style.css">
</head>

<body>

<div class="layout">

<div class="left">
{ads_html}
</div>

<div class="center">
{rss_html}
</div>

</div>

</body>
</html>
"""

open("index.html","w",encoding="utf-8").write(html)
