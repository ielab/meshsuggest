from bs4 import BeautifulSoup
import requests
import os
import time
import json


def extractWikiContent(meshJSON):
    for mesh in meshJSON:
        meshDir = os.listdir("wiki_content")
        if mesh["uid"] not in meshDir:
            term = mesh["term"]
            response = requests.get("https://en.wikipedia.org/wiki/" + term)
            print(mesh["uid"] + "   " + mesh["term"] + "    " + str(response.status_code))
            while response.content is None:
                time.sleep(1)
                response = requests.get("https://en.wikipedia.org/wiki/" + term)
                print(mesh["uid"] + "   " + mesh["term"] + "    " + str(response.status_code))
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                for script in soup('script'):
                    script.decompose()
                for style in soup('style'):
                    style.decompose()
                for link in soup('link'):
                    link.decompose()
                for meta in soup('meta'):
                    meta.decompose()
                for d in soup('div', 'noprint'):
                    d.decompose()
                for a in soup('a', 'mw-jump-link'):
                    a.decompose()
                for au in soup('div', 'authority-control'):
                    au.decompose()
                for footer in soup('div', 'printfooter'):
                    footer.decompose()
                for cat in soup('div', 'mw-hidden-catlinks'):
                    cat.decompose()
                for cat2 in soup('div', 'mw-hidden-cats-hidden'):
                    cat2.decompose()
                for nav in soup('div', 'mw-navigation'):
                    nav.decompose()
                for h in soup('div', 'body'):
                    h.decompose()
                for ref in soup('div', 'reflist'):
                    ref.decompose()
                for tb in soup('table', 'mbox-small'):
                    tb.decompose()
                for sis in soup('div', 'sistersitebox'):
                    sis.decompose()
                for links in soup('div', 'plainlinks'):
                    links.decompose()
                for nv in soup('div', 'navbox'):
                    nv.decompose()
                for f in soup('div', {'id': 'footer'}):
                    f.decompose()
                # print(soup.get_text(" ", strip=True))
                text = {
                    "text": soup.get_text(' ', strip=True)
                }
                with open('wiki_content/' + mesh["uid"], 'w+') as f:
                    json.dump(text, f)
