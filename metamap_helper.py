from atm_helper import *


def getMetaMeshTerms(path, keywordsF, meshF):
    keywordsContent = keywordsF.read()
    meshContent = meshF.read()
    oriMeshs = meshContent.split("\n")
    cleanedOriMeshs = cleanTerms(oriMeshs)
    keywords = keywordsContent.split("\n")
    generatedMeshs, objRet = requestMetaMeshs(keywords)
    generatedMeshs = cleanTerms(generatedMeshs)
    writeFile(path, "meta_progress", LINEBREAK)
    writeFile(path, "meta_progress", "Keywords: \n")
    for k in keywords:
        writeFile(path, "meta_progress", k + "\n")
    writeFile(path, "meta_progress", LINEBREAK)
    writeFile(path, "meta_progress", "Original Mesh Terms: \n")
    res = []
    seen = set()
    for oriMesh in cleanedOriMeshs:
        obj = next((x for x in MESHINFO if x["term"] == oriMesh or oriMesh in x["entry_list"]), None)
        if obj is not None:
            writeFile(path, "meta_progress", obj["uid"] + " - " + obj["term"] + "\n")
            seen.add(obj["uid"])
            res.append(obj["term"])
        else:
            suppobj = next((x for x in SUPPINFO if oriMesh in x["names"]), None)
            if suppobj is not None:
                for y in suppobj["ids"]:
                    if y not in seen:
                        obj = next((x for x in MESHINFO if x["uid"] == y), None)
                        if obj is not None:
                            writeFile(path, "meta_progress", obj["uid"] + " - " + obj["term"] + "\n")
                            res.append(obj["term"])
    writeFile(path, "meta_progress", LINEBREAK)
    writeFile(path, "meta_progress", "Generated MeSH Terms: \n")
    for i in objRet:
        writeFile(path, "meta_progress", i["uid"] + " - " + i["term"] + "\n")
    writeFile(path, "meta_progress", LINEBREAK)
    return generatedMeshs, res


def requestMetaMeshs(keywords):
    meshs = []
    objs = []
    seen = set()
    for k in keywords:
        k = MetaMapProcessK(k)
        response = requests.post(CONFIG["metamap_url"], data=k)
        while response.content is None or response.status_code is not 200:
            time.sleep(0.1)
            response = requests.post(CONFIG["metamap_url"], data=k)
        generatedMeshs, objRet, seen = parseMetaResponse(response, seen)
        if len(generatedMeshs) is not 0:
            for g in generatedMeshs:
                meshs.append(g)
        if len(objRet) is not 0:
            for i in objRet:
                objs.append(i)
    return meshs, objs


def MetaMapProcessK(k):
    k = k.replace("β", "beta")
    return k


def parseMetaResponse(response, seen):
    generatedMeshs = []
    res = json.loads(response.content)
    if res is not None:
        for item in res:
            sources = item["Sources"]
            if "MSH" in sources and item["CandidatePreferred"] is not None and item["CandidatePreferred"] is not "":
                generatedMeshs.append(item["CandidatePreferred"])
        if len(generatedMeshs) > 0:
            ret = []
            objRet = []
            cleanMesh = cleanTerms(generatedMeshs)
            for mesh in cleanMesh:
                meshobj = next((x for x in MESHINFO if x["term"] == mesh or mesh in x["entry_list"]), None)
                if meshobj is not None:
                    if meshobj["uid"] not in seen:
                        seen.add(meshobj["uid"])
                        temp1 = {
                            "uid": meshobj["uid"],
                            "term": meshobj["term"]
                        }
                        objRet.append(temp1)
                        ret.append(meshobj["term"])
                else:
                    suppobj = next((x for x in SUPPINFO if mesh in x["names"]), None)
                    if suppobj is not None:
                        for i in suppobj["ids"]:
                            if i not in seen:
                                seen.add(i)
                                obj = next((x for x in MESHINFO if x["uid"] == i), None)
                                if obj is not None:
                                    temp2 = {
                                        "uid": obj["uid"],
                                        "term": obj["term"]
                                    }
                                    objRet.append(temp2)
                                    ret.append(obj["term"])
            if len(ret) > 0:
                return cleanTerms(ret), objRet, seen
            else:
                return [], [], seen
        else:
            return [], [], seen
    else:
        return [], [], seen


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
        line = d + "_" + dd + "    " + "0" + "    " + obj["uid"] + "    " + str(
            count) + "    " + "0.00" + "    " + path + "\n"
        resFile.write(line)
        count += 1
    return count
