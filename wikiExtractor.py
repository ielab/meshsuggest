from bs4 import BeautifulSoup
import requests
import os
import hashlib
import json

NOT_FOUND = "Wikipedia does not have an article with this exact name."


def extractWikiContent(meshJSON):
    for mesh in meshJSON:
        meshDir = os.listdir("wiki_content")
        meshHashUID = hashlib.md5(mesh["uid"].encode())
        meshHashRes = meshHashUID.hexdigest()
        if meshHashRes not in meshDir:
            term = mesh["term"]
            response = requests.get("https://en.wikipedia.org/wiki/" + term)
            soup = BeautifulSoup(response.content, 'html.parser')
            allB = soup.find_all('b')
            textInB = []
            if len(allB) > 0:
                for b in allB:
                    textInB.append(b.text)
            if NOT_FOUND in textInB:
                continue
            else:
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
                for dd in soup('div', 'navbox authority-control'):
                    dd.decompose()
                for footer in soup('div', 'printfooter'):
                    footer.decompose()
                for cat in soup('div', 'mw-hidden-catlinks mw-hidden-cats-hidden'):
                    cat.decompose()
                for nav in soup('div', 'mw-navigation'):
                    nav.decompose()
                for h in soup('div', 'body'):
                    h.decompose()
                print(soup.get_text(" ", strip=True))
                # text = {
                #     "text": soup.get_text(' ', strip=True)
                # }
                # with open('wiki_content/' + meshHashRes, 'w+') as f:
                #     json.dump(text, f)
