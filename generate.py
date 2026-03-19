import feedparser
import json
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# JST用
JST_OFFSET = 9

# RSSサイト読み込み
with open("sites.json", "r", encoding="utf-8") as f:
    sites = json.load(f)

# メルカリ広告読み込み
with open("mercari.json", "r", encoding="utf-8") as f:
    mercari = json.load(f)

# ランダムで最大6件抽出
ads = random.sample(mercari, min(len(mercari), 6))

# メルカリサムネ取得関数
def get_mercari_thumbnail(url):
    try:
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        og = soup.find("meta", property="og:image")
        return og["content"] if og else ""
    except:
        return ""

# 広告HTML生成
ads_html = ""
for ad_url in ads:
    thumb = get_mercari_thumbnail(ad_url)
    if thumb:
        ads_html += f'<a href="{ad_url}" target="_blank"><img src="{thumb}"></a>'

# RSS記事HTML生成
rss_html = ""
for site in sites:
    name = site.get("name", "")
    url = site.get("url", "")
    top = site.get("top", "")

    rss_html += f'<h3><a class="site_title" href="{top}" target="_blank">{name}</a></h3><ul>'

    feed = feedparser.parse(url)

    for entry in feed.entries[:7]:
        time_str = "--:--"
        t = None

        if hasattr(entry, "published_parsed") and entry.published_parsed:
            t = datetime(*entry.published_parsed[:6]) + timedelta(hours=JST_OFFSET)
        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
            t = datetime(*entry.updated_parsed[:6]) + timedelta(hours=JST_OFFSET)

        if t:
            time_str = t.strftime("%m/%d %H:%M")

        rss_html += f'<li><span class="time">{time_str}</span> <a href="{entry.link}" target="_blank">{entry.title}</a></li>'

    rss_html += "</ul>"

# HTML構造
html = f"""
<html>
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="style.css">
<title>RSSまとめサイト</title>
</head>
<body>

<h1>RSSまとめサイト</h1>

<div class="container">
    <div class="left">
        {ads_html}
    </div>
    <div class="main">
        {rss_html}
    </div>
</div>

</body>
</html>
"""

# index.htmlに書き出し
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
