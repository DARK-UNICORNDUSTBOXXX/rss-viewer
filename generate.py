import feedparser
import json
import random
from datetime import datetime

# RSSサイト読み込み
with open("sites.json",encoding="utf-8") as f:
    sites=json.load(f)

# メルカリ広告読み込み
with open("mercari.json",encoding="utf-8") as f:
    mercari=json.load(f)

ads=random.sample(mercari,min(len(mercari),6))

rss_html=""

for site in sites:

    feed=feedparser.parse(site["url"])

    rss_html+=f"<h2>{site['name']}</h2>"
    rss_html+="<ul>"

    for entry in feed.entries[:10]:

        title=entry.title
        link=entry.link

        if hasattr(entry,"published_parsed"):
            time=datetime(*entry.published_parsed[:6]).strftime("%m/%d %H:%M")
        else:
            time=""

        rss_html+=f'''
<li>
<span class="time">{time}</span>
<a href="{link}" target="_blank">{title}</a>
</li>
'''

    rss_html+="</ul>"

# 広告HTML
ads_html='<a href="https://jp.mercari.com/search?afid=2445940742&keyword=%E5%88%9D%E9%9F%B3%E3%83%9F%E3%82%AF+%E3%83%95%E3%82%A3%E3%82%AE%E3%83%A5%E3%82%A2" target="_blank">'

for img in ads:
    ads_html+=f'<img src="{img}">'

ads_html+='</a>'

# HTML生成
html=f'''
<html>
<head>
<meta charset="utf-8">
<title>RSSまとめ</title>
<link rel="stylesheet" href="style.css">
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
'''

open("index.html","w",encoding="utf-8").write(html)
