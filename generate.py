import feedparser
import json
from datetime import datetime

with open("sites.json","r",encoding="utf-8") as f:
    sites=json.load(f)

html="""
<html>
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="style.css">
<title>2chまとめアンテナ</title>
</head>
<body>
<h1>2chまとめアンテナ</h1>
"""

for site in sites:

    html+=f"<h3>{site['name']}</h3><ul>"

    feed=feedparser.parse(site["url"])

    for entry in feed.entries[:7]:

        time="--:--"
        t=None

        if "published_parsed" in entry and entry.published_parsed:
            t=datetime(*entry.published_parsed[:6])

        elif "updated_parsed" in entry and entry.updated_parsed:
            t=datetime(*entry.updated_parsed[:6])

        elif "created_parsed" in entry and entry.created_parsed:
            t=datetime(*entry.created_parsed[:6])

        if t:
            time=t.strftime("%m/%d %H:%M")

        html+=f"""
<li>
<span class="time">{time}</span>
<a href="{entry.link}" target="_blank">{entry.title}</a>
</li>
"""

    html+="</ul>"

html+="</body></html>"

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)
