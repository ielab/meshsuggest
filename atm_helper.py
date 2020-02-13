import shutil
import requests
import json
import time

SYMBOLS = ['*', '"', '[MeSH Terms]']
LINEBREAK = "---------------------------------------------------------\n"


def readFile(path, mode, file):
    if mode is "c":
        queryContent = file.read()
        writeFile(path, "atm_progress", LINEBREAK)
        writeFile(path, "atm_progress", "Sub-Clause Content: \n" + queryContent + "\n")
        generatedMesh, cleaned = requestForSearchDetails(path, queryContent)
        return generatedMesh, cleaned
    else:
        meshContent = file.read()
        meshs = meshContent.split("\n")
        cleanedMeshs = cleanTerms(meshs)
        writeFile(path, "atm_progress", LINEBREAK)
        writeFile(path, "atm_progress", "Original MeSH Terms: \n")
        for mesh in cleanedMeshs:
            writeFile(path, "atm_progress", mesh + "\n")
        return cleanedMeshs


def requestForSearchDetails(path, query):
    configF = open("config.json", "r")
    config = json.loads(configF.read())
    url = config["url"] + "?db=pubmed&api_key=" + config["key"] + "&retmode=json&term=" + query
    response = timeoutReq(url)
    res = json.loads(response.content)
    translationStack = res["esearchresult"]["translationstack"]
    generatedMesh, cleaned = getATMMeSHTerms(translationStack)
    writeFile(path, "atm_progress", LINEBREAK)
    writeFile(path, "atm_progress", "Generated MeSH Terms: \n")
    for mesh in generatedMesh:
        writeFile(path, "atm_progress", mesh + "\n")
    return generatedMesh, cleaned


def timeoutReq(url):
    time.sleep(1)
    response = requests.get(url, params=None)
    return response


def cleanTerms(bucket):
    res = []
    for item in bucket:
        for char in SYMBOLS:
            item = item.replace(char, "")
        res.append(item.lower())
    res = list(dict.fromkeys(res))
    return res


def getATMMeSHTerms(translationstack):
    mesh = []
    cleanedMesh = []
    res = []
    seen_term = set()
    noDupMesh = []
    for item in translationstack:
        if type(item) is not str and item["field"] == "MeSH Terms":
            term = {
                "term": item["term"],
                "explode": item["explode"]
            }
            mesh.append(term)
    for t in mesh:
        for char in SYMBOLS:
            t["term"] = t["term"].replace(char, "")
        t["term"] = t["term"].lower()
        cleanedMesh.append(t)
        res.append(t["term"])
    for d in cleanedMesh:
        if d["term"] not in seen_term:
            noDupMesh.append(d)
            seen_term.add(d["term"])
    res = cleanTerms(res)
    return res, noDupMesh


def findMatch(original, generated):
    hitMesh = set(original) & set(generated)
    return hitMesh


def writeFile(path, filename, data):
    f = open(path + "/" + filename, "a+")
    f.write(data)
    return


def getOriginalQuery(path):
    meshQF = open(path + "/" + "clause_mesh", "r")
    meshQContent = meshQF.read()
    return meshQContent


def generateNewQuery(path, meshs):
    noMeshQF = open(path + "/" + "clause_no_mesh", "r")
    noMeshContent = noMeshQF.read()
    if len(meshs) > 0:
        allMesh = []
        for t in meshs:
            if t["explode"] is "Y":
                t["term"] = t["term"] + "[mesh]"
            else:
                t["term"] = t["term"] + "[mesh:noexp]"
        for m in meshs:
            allMesh.append(m["term"])
        meshQuery = " OR ".join(allMesh)
        newQuery = "(" + meshQuery + " OR " + noMeshContent[1:]
        return newQuery
    else:
        return noMeshContent


# From https://gist.github.com/greenstick/b23e475d2bfdc3a82e34eaa1f6781ee4
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', autosize=False):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    if autosize:
        cols, _ = shutil.get_terminal_size(fallback=(length, 1))
        length = cols - len(styling)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s' % styling.replace(fill, bar), end='\r')
    if iteration == total:
        print()


def lineSeperator(fill='#', length=100):
    styling = '%s' % fill
    cols, _ = shutil.get_terminal_size(fallback=(length, 1))
    length = cols - len(styling)
    bar = fill * length
    print('\r%s' % styling.replace(fill, bar), end='\r')
    print()
