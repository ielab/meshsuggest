from metamap_helper import *


def getUMLSMeshTerms(path, keywordf, meshf, num):
    keywordsContent = keywordf.read()
    meshContent = meshf.read()
    oriMeshs = meshContent.split("\n")
    cleanedOriMeshs = cleanTerms(oriMeshs)
    keywords = keywordsContent.split("\n")
    generatedMeshs, objRet = requestUMLSMeshs(keywords, num)
    generatedMeshs = cleanTerms(generatedMeshs)
    writeFile(path, "umls_progress_" + num, LINEBREAK)
    writeFile(path, "umls_progress_" + num, "Keywords: \n")
    for k in keywords:
        writeFile(path, "umls_progress_" + num, k + "\n")
    writeFile(path, "umls_progress_" + num, LINEBREAK)
    writeFile(path, "umls_progress_" + num, "Original Mesh Terms: \n")
    res = []
    seen = set()
    for oriMesh in cleanedOriMeshs:
        obj = next((x for x in MESHINFO if x["term"] == oriMesh or oriMesh in x["entry_list"]), None)
        if obj is not None:
            writeFile(path, "umls_progress_" + num, obj["uid"] + " - " + obj["term"] + "\n")
            seen.add(obj["uid"])
            res.append(obj["term"])
        else:
            suppobj = next((x for x in SUPPINFO if oriMesh in x["names"]), None)
            if suppobj is not None:
                for y in suppobj["ids"]:
                    if y not in seen:
                        obj = next((x for x in MESHINFO if x["uid"] == y), None)
                        if obj is not None:
                            writeFile(path, "umls_progress_" + num, obj["uid"] + " - " + obj["term"] + "\n")
                            res.append(obj["term"])
    writeFile(path, "umls_progress_" + num, LINEBREAK)
    writeFile(path, "umls_progress_" + num, "Generated MeSH Terms: \n")
    for i in objRet:
        writeFile(path, "umls_progress_" + num, i["uid"] + " - " + i["term"] + "\n")
    writeFile(path, "umls_progress_" + num, LINEBREAK)
    return generatedMeshs, objRet, res


def requestUMLSMeshs(keywords, num):
    meshs = []
    objs = []
    generatedMeshs, objRet = processCutoffMeshs(keywords, num)
    if len(generatedMeshs) is not 0:
        for g in generatedMeshs:
            meshs.append(g)
    if len(objRet) is not 0:
        for i in objRet:
            objs.append(i)
    return meshs, objs


def processCutoffMeshs(keywords, num):
    runList = []
    for key in keywords:
        seen = set()
        scores = []
        generatedObj = []
        finalObjs = []
        noDupObjs = []
        hashK = hashlib.md5(key.encode())
        hashKRes = hashK.hexdigest()
        responseF = open("umls_responses/" + hashKRes, "r")
        response = responseF.read()
        resContent = json.loads(response)
        if resContent is not None:
            hits = resContent["hits"]["hits"]
            if len(hits) > 0:
                for hit in hits:
                    thesaurus = hit["_source"]["thesaurus"]
                    for each in thesaurus:
                        if each["MRCONSO_LAT"] == "ENG":
                            if each["MRCONSO_SAB"] == "MSH" or each["MRDEF_SAB"] == "MSH":
                                if each["MRCONSO_STR"] is not None and each["MRCONSO_STR"] != "":
                                    temp1 = {
                                        "score": float(hit["_score"]),
                                        "term": each["MRCONSO_STR"].lower()
                                    }
                                    generatedObj.append(temp1)
        if len(generatedObj) > 0:
            for obj in generatedObj:
                found = checkTermExistence(obj["term"])
                if len(found) > 0:
                    for f in found:
                        if f["uid"] not in seen:
                            temp2 = {
                                "score": float(obj["score"]),
                                "uid": f["uid"],
                                "term": f["term"].lower()
                            }
                            scores.append(float(obj["score"]))
                            seen.add(f["uid"])
                            finalObjs.append(temp2)
        if len(finalObjs) > 0:
            maxScore = max(scores)
            minScore = min(scores)
            for o in finalObjs:
                if maxScore != minScore:
                    t = {
                        "uid": o["uid"],
                        "term": o["term"],
                        "score": float((o["score"] - minScore) / (maxScore - minScore))
                    }
                else:
                    t = {
                        "uid": o["uid"],
                        "term": o["term"],
                        "score": 1.00
                    }
                noDupObjs.append(t)
        if len(noDupObjs) > 0:
            runList.append(noDupObjs)
    if len(runList) > 0:
        fusedList = performCombSUM(runList)
        totalScore = 0
        fuseScoreList = []
        for s in fusedList:
            fuseScoreList.append(s["score"])
        maxFusedScore = max(fuseScoreList)
        invertedList = []
        for fused in fusedList:
            temp = {
                "term": fused["term"],
                "uid": fused["uid"],
                "score": maxFusedScore - float(fused["score"])
            }
            invertedList.append(temp)
        invertedList.sort(key=lambda x: x["score"], reverse=False)
        if num == "one":
            cutoffList = []
            mh = []
            for t in invertedList:
                if float(t["score"]) == float(0):
                    cutoffList.append(t)
            if len(cutoffList) > 0:
                sortedCutoffList = sortList(cutoffList)
                for each in sortedCutoffList:
                    mh.append(each["term"])
                return mh, sortedCutoffList
            else:
                return [], []
        else:
            for t in fusedList:
                totalScore += float(t["score"])
            cutoffList = []
            mh = []
            cutoff = float(num) / 100.00
            cutoffScore = totalScore * cutoff
            tempTotal = 0.00
            for z in invertedList:
                tempTotal += float(z["score"])
                if tempTotal <= cutoffScore:
                    cutoffList.append(z)
            if len(cutoffList) > 0:
                cutoffList.sort(key=lambda x: x["score"], reverse=False)
                sortedCutoffList = sortList(cutoffList)
                for each in sortedCutoffList:
                    mh.append(each["term"])
                return mh, sortedCutoffList
            else:
                return [], []
    else:
        return [], []


def performCombSUM(runList):
    if len(runList) == 1:
        return runList[0]
    elif len(runList) > 1:
        finalRes = []
        uidList = []
        grouped = []
        seenUID = set()
        for run in runList:
            for k in run:
                if k["uid"] not in seenUID:
                    uidList.append(k["uid"])
                    seenUID.add(k["uid"])
        for uniqueID in uidList:
            single = []
            for run in runList:
                for item in run:
                    if item["uid"] == uniqueID:
                        single.append(item)
            grouped.append(single)
        for each in grouped:
            if len(each) == 1:
                finalRes.append(each[0])
            else:
                score = 0.00
                for e in each:
                    score += float(e["score"])
                line = {
                    "term": str(each[0]["term"]),
                    "uid": str(each[0]["uid"]),
                    "score": float(score)
                }
                finalRes.append(line)
        finalRes.sort(key=lambda x: x["score"], reverse=True)
        return finalRes
    else:
        return []


def checkTermExistence(term):
    found = []
    meshobj = next((x for x in MESHINFO if x["term"] == term or term in x["entry_list"]), None)
    if meshobj is not None:
        temp1 = {
            "uid": meshobj["uid"],
            "term": meshobj["term"]
        }
        found.append(temp1)
    else:
        suppobj = next((x for x in SUPPINFO if term in x["names"]), None)
        if suppobj is not None:
            for i in suppobj["ids"]:
                obj = next((x for x in MESHINFO if x["uid"] == i), None)
                if obj is not None:
                    temp2 = {
                        "uid": obj["uid"],
                        "term": obj["term"]
                    }
                    found.append(temp2)
    return found


def createUMLSResFile(path, d, dd, generatedMesh, num):
    resFile = open(path + "/" + "umls_" + num + ".res", "a+")
    count = 1
    for mesh in generatedMesh:
        obj = next((x for x in MESHINFO if x["term"] == mesh["term"] or mesh["term"] in x["entry_list"]), None)
        line = d + "_" + dd + "    " + "0" + "    " + obj["uid"] + "    " + str(
            count) + "    " + str(mesh["score"]) + "    " + path + "\n"
        resFile.write(line)
        count += 1


def generateNewUMLSQuery(path, meshs):
    noMeshQF = open(path + "/" + "clause_no_mesh", "r")
    noMeshContent = noMeshQF.read()
    if len(meshs) > 0:
        meshQuery = "[mesh] OR ".join(meshs)
        newQuery = "(" + meshQuery + "[mesh] OR " + noMeshContent[1:]
    else:
        newQuery = noMeshContent
    return newQuery
