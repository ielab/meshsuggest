import requests
import os
import time
import json
from atm_helper import CONFIG


def writeUMLSAndMetaResponse(keywordsF):
    keywordsContent = keywordsF.read()
    keywords = keywordsContent.split("\n")
    for keyword in keywords:
        k = MetaMapProcessK(keyword)
        response = requests.post(CONFIG["metamap_url"], data=k)
        print("MetaMap: " + keyword + " " + str(response.status_code))
        while response.content is None or response.status_code is not 200:
            time.sleep(0.2)
            response = requests.post(CONFIG["metamap_url"], data=k)
            print("MetaMap: " + keyword + " " + str(response.status_code))
        with open("metamap_responses/" + str(hash(keyword)) + ".json", "w+") as f:
            json.dump(json.loads(response.content), f)
    for key in keywords:
        umlsk = UMLSProcessK(key)
        param = {
            "q": umlsk
        }
        umlsresponse = requests.get(CONFIG["umls_url"], params=param, auth=(CONFIG["username"], CONFIG["secret"]))
        print("UMLS: " + key + " " + str(umlsresponse.status_code))
        while umlsresponse.content is None or umlsresponse.status_code is not 200:
            time.sleep(0.2)
            umlsresponse = requests.get(CONFIG["umls_url"], params=param, auth=(CONFIG["username"], CONFIG["secret"]))
            print("UMLS: " + key + " " + str(umlsresponse.status_code))
        with open("umls_responses/" + str(hash(key)) + ".json", "w+") as f:
            json.dump(json.loads(umlsresponse.content), f)


def MetaMapProcessK(k):
    k = k.replace("β", "beta")
    return k


def UMLSProcessK(k):
    k = k.replace("/", "\/")
    k = k.replace("[", "")
    k = k.replace("]", " ")
    return k
