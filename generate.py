import feedparser
import requests
from bs4 import BeautifulSoup
import html

rss_list = {
    "fig速": "https://figsoku.net/blog-feed.xml",
    "電撃ホビー": "https://hobby.dengeki.com/feed/",
    "ホビーサーチ": "https://www.1999.co.jp/blog/feed"
}

def get_thumbnail(url):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        og = soup.find("meta", property="og:image")
        if og:
            return og["content"]

        img = soup.find("img")
        if img:
            return img["src"]

    except:
        pass

    return ""

html_output = ""

for site, rss in rss_list.items():

    html_output += f'<div class="rss-site">\n'
    html_output += f'<div class="rss-site-title">{site}</div>\n'

    feed = feedparser.parse(rss)

    for entry in feed.entries[:15]:

        title = html.escape(entry.title)
        link = entry.link

        thumb = get_thumbnail(link)

        html_output += '<div class="rss-item">\n'

        if thumb:
            html_output += f'<a href="{link}" target="_blank"><img class="rss-thumb" src="{thumb}"></a>\n'

        html_output += f'''
        <div class="rss-title">
        <a href="{link}" target="_blank">{title}</a>
        </div>
        '''

        html_output += '</div>\n'

    html_output += "</div>\n"


with open("rss.html", "w", encoding="utf-8") as f:
    f.write(html_output)
