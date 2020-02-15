from atm_helper import *


def getMetaMeshTerms(path, keywordsF, meshF):
    keywordsContent = keywordsF.read()
    meshContent = meshF.read()
    oriMeshs = meshContent.split("\n")
    cleanedOriMeshs = cleanTerms(oriMeshs)
    keywords = keywordsContent.split("\n")
    generatedMeshs = cleanTerms(requestMetaMeshs(keywords))
    writeFile(path, "meta_progress", LINEBREAK)
    writeFile(path, "meta_progress", "Keywords: \n")
    for k in keywords:
        writeFile(path, "meta_progress", k + "\n")
    writeFile(path, "meta_progress", LINEBREAK)
    writeFile(path, "meta_progress", "Original Mesh Terms: \n")
    for oriMesh in cleanedOriMeshs:
        writeFile(path, "meta_progress", oriMesh + "\n")
    writeFile(path, "meta_progress", LINEBREAK)
    writeFile(path, "meta_progress", "Generated MeSH Terms: \n")
    for i in generatedMeshs:
        writeFile(path, "meta_progress", i + "\n")
    writeFile(path, "meta_progress", LINEBREAK)
    return generatedMeshs, cleanedOriMeshs


def requestMetaMeshs(keywords):
    meshs = []
    for k in keywords:
        time.sleep(0.1)
        response = requests.post(CONFIG["metamap_url"], data=k)
        while response.content is None or response.status_code is not 200:
            response = requests.post(CONFIG["metamap_url"], data=k)
        generatedMeshs = parseMetaResponse(response)
        if len(generatedMeshs) is not 0:
            for g in generatedMeshs:
                meshs.append(g)
    return meshs


def parseMetaResponse(response):
    generatedMeshs = []
    res = json.loads(response.content)
    if res is not None:
        for item in res:
            sources = item["Sources"]
            if "MSH" in sources and item["CandidatePreferred"] is not None and item["CandidatePreferred"] is not "":
                generatedMeshs.append(item["CandidatePreferred"])
        if len(generatedMeshs) is not 0:
            ret = []
            cleanMesh = cleanTerms(generatedMeshs)
            for mesh in cleanMesh:
                meshobj = next((x for x in MESHINFO if x["term"] == mesh or mesh in x["entry_list"]), None)
                if meshobj is not None:
                    ret.append(mesh)
                else:
                    suppobj = next((x for x in SUPPINFO if mesh in x["names"]), None)
                    if suppobj is not None:
                        ret.append(mesh)
            if len(ret) > 0:
                return cleanTerms(ret)
            else:
                return []
        else:
            return generatedMeshs
    else:
        return generatedMeshs


def generateNewMetaQuery(path, meshs):
    noMeshQF = open(path + "/" + "clause_no_mesh", "r")
    noMeshContent = noMeshQF.read()
    if len(meshs) > 0:
        meshQuery = "[mesh] OR ".join(meshs)
        newQuery = "(" + meshQuery + "[mesh] OR " + noMeshContent[1:]
    else:
        newQuery = noMeshContent
    return newQuery


def createMetaResFile(path, d, dd, generatedMesh, count):
    resFile = open(path + "/" + "meta.res", "a+")
    for mesh in generatedMesh:
        obj = next((x for x in MESHINFO if x["term"] == mesh or mesh in x["entry_list"]), None)
        if obj is not None:
            line = d + "_" + dd + "    " + "0" + "    " + obj["uid"] + "    " + str(
                count) + "    " + "0.00" + "    " + path + "\n"
            resFile.write(line)
            count += 1
        else:
            suppobj = next((x for x in SUPPINFO if mesh in x["names"]), None)
            if suppobj is not None:
                ids = suppobj["ids"]
                for n in ids:
                    line = d + "_" + dd + "    " + "0" + "    " + n + "    " + str(
                        count) + "    " + "0.00" + "    " + path + "\n"
                    resFile.write(line)
                    count += 1
            else:
                print(mesh)
    return count
