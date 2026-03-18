import feedparser
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# 日本時間
JST = timezone(timedelta(hours=9))

# サイト読み込み
with open("sites.json","r",encoding="utf-8") as f:
    sites=json.load(f)

# ----------------------------
# メルカリ画像取得
# ----------------------------

mercari_url="https://jp.mercari.com/search?afid=2445940742&keyword=%E5%88%9D%E9%9F%B3%E3%83%9F%E3%82%AF+%E3%83%95%E3%82%A3%E3%82%AE%E3%83%A5%E3%82%A2"

img_list=[]

try:

    r=requests.get(mercari_url,headers={"User-Agent":"Mozilla/5.0"})
    soup=BeautifulSoup(r.text,"html.parser")

    imgs=soup.find_all("img")

    for img in imgs:

        src=img.get("src")

        if src and "static.mercdn.net" in src:

            img_list.append(src)

        if len(img_list)>=30:
            break

except:
    pass


with open("mercari.json","w",encoding="utf-8") as f:
    json.dump(img_list,f,ensure_ascii=False,indent=2)

# ----------------------------
# HTML生成
# ----------------------------

html="""
<html>
<head>
<meta charset="UTF-8">
<title>2chまとめアンテナ</title>
<link rel="stylesheet" href="style.css">
</head>
<body>

<div id="mercari_side"></div>

<h1>2chまとめアンテナ</h1>

"""

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
            t=t.astimezone(JST)
            time=t.strftime("%m/%d %H:%M")

        html+=f"""
<li>
<span class="time">{time}</span>
<a href="{entry.link}" target="_blank">{entry.title}</a>
</li>
"""

    html+="</ul>"

html+="""

<script>

fetch("mercari.json")
.then(r=>r.json())
.then(list=>{

const area=document.getElementById("mercari_side")

const shuffled=list.sort(()=>0.5-Math.random()).slice(0,6)

shuffled.forEach(img=>{

const a=document.createElement("a")
a.href="https://jp.mercari.com/search?afid=2445940742&keyword=%E5%88%9D%E9%9F%B3%E3%83%9F%E3%82%AF+%E3%83%95%E3%82%A3%E3%82%AE%E3%83%A5%E3%82%A2"
a.target="_blank"

const image=document.createElement("img")
image.src=img
image.className="mercari_img"

a.appendChild(image)
area.appendChild(a)

})

})

</script>

</body>
</html>
"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)
