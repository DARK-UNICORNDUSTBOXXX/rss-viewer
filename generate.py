import feedparser
import json
import random
from datetime import datetime, timedelta, timezone

# 日本時間
JST = timezone(timedelta(hours=9))

# RSSサイト読み込み
with open("sites.json","r",encoding="utf-8") as f:
    sites=json.load(f)

# メルカリ画像読み込み
with open("mercari.json","r",encoding="utf-8") as f:
    mercari=json.load(f)

# ランダム画像
ads=random.sample(mercari, min(6,len(mercari)))

html="""
<html>
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="style.css">
<title>2chまとめアンテナ</title>
</head>
<body>

<div class="left_ads">
"""

# メルカリ画像表示
for img in ads:
    html+=f'<a href="{img["url"]}" target="_blank"><img src="{img["img"]}"></a>'

html+="""
</div>

<h1>2chまとめアンテナ</h1>
"""

# RSS取得
for site in sites:

    html+=f'<h3><a href="{site["top"]}" target="_blank">{site["name"]}</a></h3><ul>'

    feed=feedparser.parse(site["url"])

    for entry in feed.entries[:7]:

        time="--:--"
        t=None

        if hasattr(entry,"published_parsed") and entry.published_parsed:
            t=datetime(*entry.published_parsed[:6],tzinfo=timezone.utc)

        elif hasattr(entry,"updated_parsed") and entry.updated_parsed:
            t=datetime(*entry.updated_parsed[:6],tzinfo=timezone.utc)

        if t:
            time=t.astimezone(JST).strftime("%m/%d %H:%M")

        html+=f"""
<li>
<span class="time">{time}</span>
<a href="{entry.link}" target="_blank">{entry.title}</a>
</li>
"""

    html+="</ul>"

html+="</body></html>"

# HTML書き出し
with open("index.html","w",encoding="utf-8") as f:
    f.write(html)
