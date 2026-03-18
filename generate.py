import feedparser
import json
import random
import html
import requests
from bs4 import BeautifulSoup

# ------------------------
# RSS読み込み
# ------------------------

with open("sites.json", encoding="utf-8") as f:
    sites = json.load(f)

# ------------------------
# メルカリ画像取得
# ------------------------

SEARCH_URL = "https://jp.mercari.com/search?keyword=初音ミク フィギュア"
AFF_LINK = "https://jp.mercari.com/search?afid=2445940742&keyword=%E5%88%9D%E9%9F%B3%E3%83%9F%E3%82%AF+%E3%83%95%E3%82%A3%E3%82%AE%E3%83%A5%E3%82%A2"

imgs = []

try:

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(SEARCH_URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for img in soup.find_all("img"):

        src = img.get("src")

        if src and "mercari" in src and "item" in src:
            imgs.append(src)

except:
    pass

# 6枚ランダム
ads = random.sample(imgs, min(6, len(imgs)))

# ------------------------
# HTML生成
# ------------------------

html_out = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>RSSまとめ</title>
<link rel="stylesheet" href="style.css">
</head>

<body>

<h1>RSSまとめ</h1>

<div class="container">

<div class="left">
"""

# ------------------------
# 広告
# ------------------------

html_out += f'<a href="{AFF_LINK}" target="_blank">'

for img in ads:
    html_out += f'<img src="{img}">'

html_out += "</a></div>"

# ------------------------
# RSSカラム
# ------------------------

html_out += '<div class="main">'

for site in sites:

    name = site["name"]
    url = site["url"]
    top = site["top"]

    feed = feedparser.parse(url)

    html_out += f"<h3>{html.escape(name)}</h3>"
    html_out += "<ul>"

    for entry in feed.entries[:top]:

        title = html.escape(entry.title)
        link = entry.link

        html_out += f'<li><a href="{link}" target="_blank">{title}</a></li>'

    html_out += "</ul>"

html_out += "</div></div></body></html>"

# ------------------------
# 出力
# ------------------------

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_out)
