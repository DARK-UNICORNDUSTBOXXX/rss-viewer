import feedparser
import json
import random
import asyncio
from playwright.async_api import async_playwright

# -----------------------------
# RSSサイト読み込み
# -----------------------------
with open("sites.json","r",encoding="utf-8") as f:
    sites=json.load(f)

# -----------------------------
# メルカリ画像取得
# -----------------------------
async def get_mercari_images():

    url="https://jp.mercari.com/search?keyword=初音ミク フィギュア"

    images=[]

    async with async_playwright() as p:

        browser=await p.chromium.launch()
        page=await browser.new_page()

        await page.goto(url)

        await page.wait_for_selector("img")

        imgs=await page.query_selector_all("img")

        for img in imgs:

            src=await img.get_attribute("src")

            if src and "mercdn" in src:

                images.append(src)

        await browser.close()

    images=list(set(images))

    if len(images)>6:
        images=random.sample(images,6)

    return images


# -----------------------------
# RSS取得
# -----------------------------
def get_rss():

    items=[]

    for s in sites:

        feed=feedparser.parse(s["url"])

        for e in feed.entries[:10]:

            items.append({
                "title":e.title,
                "link":e.link,
                "site":s["name"]
            })

    return items


# -----------------------------
# HTML生成
# -----------------------------
async def main():

    mercari=await get_mercari_images()
    rss=get_rss()

    html="""
<html>
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="style.css">
<title>RSS Viewer</title>
</head>

<body>

<div class="container">

<div class="left">
"""

    for img in mercari:

        html+=f"""
<a href="https://jp.mercari.com/search?afid=2445940742&keyword=%E5%88%9D%E9%9F%B3%E3%83%9F%E3%82%AF+%E3%83%95%E3%82%A3%E3%82%AE%E3%83%A5%E3%82%A2" target="_blank">
<img src="{img}">
</a>
"""

    html+="""
</div>

<div class="main">

<h1>RSSまとめ</h1>
<ul>
"""

    for r in rss:

        html+=f"""
<li>
<a href="{r["link"]}" target="_blank">
{r["title"]}
</a>
</li>
"""

    html+="""
</ul>

</div>

</div>

</body>
</html>
"""

    with open("index.html","w",encoding="utf-8") as f:
        f.write(html)


asyncio.run(main())
