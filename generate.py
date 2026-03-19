import feedparser
import json
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

JST_OFFSET = 9

# RSSサイト読み込み
with open("sites.json", "r", encoding="utf-8") as f:
    sites = json.load(f)

# アフィURL読み込み
with open("mercari.json", "r", encoding="utf-8") as f:
    affi_urls = json.load(f)

# アフィURLからサムネ画像を取得
def get_mercari_thumbnails(search_url):
    try:
        resp = requests.get(search_url, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        # 商品サムネ一覧を取得
        images = [meta["content"] for meta in soup.find_all("meta", property="og:image") if "content" in meta.attrs]
        return images
    except:
        return []

# 全アフィURLからサムネを集めてランダム選択
all_thumbs = []
for url in affi_urls:
    thumbs = get_mercari_thumbnails(url)
    all_thumbs.extend(thumbs)

# 広告用に最大6枚ランダム抽出
ads = random.sample(all_thumbs, min(len(all_thumbs), 6))

ads_html = ""
for img in ads:
    # リンクは最初のアフィURLに統一
    ads_html += f'<a href="{affi_urls[0]}" target="_blank"><img src="{img}"></a>'

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

# HTML出力
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

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
import feedparser
import json
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

JST_OFFSET = 9

# RSSサイト読み込み
with open("sites.json", "r", encoding="utf-8") as f:
    sites = json.load(f)

# アフィURL読み込み
with open("mercari.json", "r", encoding="utf-8") as f:
    affi_urls = json.load(f)

# アフィURLからサムネ画像を取得
def get_mercari_thumbnails(search_url):
    try:
        resp = requests.get(search_url, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        # 商品サムネ一覧を取得
        images = [meta["content"] for meta in soup.find_all("meta", property="og:image") if "content" in meta.attrs]
        return images
    except:
        return []

# 全アフィURLからサムネを集めてランダム選択
all_thumbs = []
for url in affi_urls:
    thumbs = get_mercari_thumbnails(url)
    all_thumbs.extend(thumbs)

# 広告用に最大6枚ランダム抽出
ads = random.sample(all_thumbs, min(len(all_thumbs), 6))

ads_html = ""
for img in ads:
    # リンクは最初のアフィURLに統一
    ads_html += f'<a href="{affi_urls[0]}" target="_blank"><img src="{img}"></a>'

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

# HTML出力
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

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
