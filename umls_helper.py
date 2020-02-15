from atm_helper import *


def getUMLSMeshTerms(path, keywordf, meshf):
    keywordsContent = keywordf.read()
    meshContent = meshf.read()
    oriMeshs = meshContent.split("\n")
    cleanedOriMeshs = cleanTerms(oriMeshs)
    keywords = keywordsContent.split("\n")
    generatedMeshs = cleanTerms(requestUMLSMeshs(keywords))
    writeFile(path, "umls_progress", LINEBREAK)
    writeFile(path, "umls_progress", "Keywords: \n")
    for k in keywords:
        writeFile(path, "umls_progress", k + "\n")
    writeFile(path, "umls_progress", LINEBREAK)
    writeFile(path, "umls_progress", "Original Mesh Terms: \n")
    for oriMesh in cleanedOriMeshs:
        writeFile(path, "umls_progress", oriMesh + "\n")
    writeFile(path, "umls_progress", LINEBREAK)
    writeFile(path, "umls_progress", "Generated MeSH Terms: \n")
    for i in generatedMeshs:
        writeFile(path, "umls_progress", i + "\n")
    writeFile(path, "umls_progress", LINEBREAK)
    return generatedMeshs, cleanedOriMeshs


def requestUMLSMeshs(keywords):
    meshs = []
    for k in keywords:
        time.sleep(0.1)
        param = {
            "q": k
        }
        response = requests.get(CONFIG["umls_url"], params=param, auth=(CONFIG["username"], CONFIG["secret"]))
        while response.content is None or response.status_code is not 200:
            response = requests.get(CONFIG["umls_url"], params=param, auth=(CONFIG["username"], CONFIG["secret"]))
        generatedMeshs = parseUMLSResponse(response)
        if len(generatedMeshs) is not 0:
            for g in generatedMeshs:
                meshs.append(g)
    return meshs


def parseUMLSResponse(response):
    meshs = []
    resContent = json.loads(response.content)
    hits = resContent["hits"]["hits"]
    for hit in hits:
        thesaurus = hit["_source"]["thesaurus"]
        for each in thesaurus:
            if each["MRCONSO_LAT"] == "ENG":
                if each["MRCONSO_SAB"] == "MSH" or each["MRDEF_SAB"] == "MSH":
                    if each["MRCONSO_STR"] is not None and each["MRCONSO_STR"] != "":
                        meshs.append(each["MRCONSO_STR"])
    meshs = cleanTerms(meshs)
    res = []
    if len(meshs) > 0:
        for mesh in meshs:
            obj = next((x for x in MESHINFO if x["term"] == mesh or mesh in x["entry_list"]), None)
            if obj is not None:
                res.append(mesh)
            else:
                suppObj = next((x for x in SUPPINFO if mesh in x["names"]), None)
                if suppObj is not None:
                    res.append(mesh)
        return res
    else:
        return []


def createUMLSResFile(path, d, dd, generatedMesh, count):
    seen = set()
    resFile = open(path + "/" + "umls.res", "a+")
    for mesh in generatedMesh:
        obj = next((x for x in MESHINFO if x["term"] == mesh or mesh in x["entry_list"]), None)
        if obj is not None:
            if obj["uid"] not in seen:
                line = d + "_" + dd + "    " + "0" + "    " + obj["uid"] + "    " + str(
                    count) + "    " + "0.00" + "    " + path + "\n"
                resFile.write(line)
                count += 1
                seen.add(obj["uid"])
        else:
            suppobj = next((x for x in SUPPINFO if mesh in x["names"]), None)
            if suppobj is not None:
                ids = suppobj["ids"]
                for n in ids:
                    if n not in seen:
                        line = d + "_" + dd + "    " + "0" + "    " + n + "    " + str(
                            count) + "    " + "0.00" + "    " + path + "\n"
                        resFile.write(line)
                        count += 1
                        seen.add(n)
    return count


def generateNewUMLSQuery(path, meshs):
    noMeshQF = open(path + "/" + "clause_no_mesh", "r")
    noMeshContent = noMeshQF.read()
    if len(meshs) > 0:
        meshQuery = "[mesh] OR ".join(meshs)
        newQuery = "(" + meshQuery + "[mesh] OR " + noMeshContent[1:]
    else:
        newQuery = noMeshContent
    return newQuery
