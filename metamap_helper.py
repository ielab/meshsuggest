from atm_helper import *
import hashlib


def getMetaMeshTerms(path, keywordsF, meshF, num):
    keywordsContent = keywordsF.read()
    meshContent = meshF.read()
    oriMeshs = meshContent.split("\n")
    cleanedOriMeshs = cleanTerms(oriMeshs)
    keywords = keywordsContent.split("\n")
    generatedMeshs, objRet = requestMetaMeshs(keywords, num)
    generatedMeshs = cleanTerms(generatedMeshs)
    writeFile(path, "meta_progress_" + num, LINEBREAK)
    writeFile(path, "meta_progress_" + num, "Keywords: \n")
    for k in keywords:
        writeFile(path, "meta_progress_" + num, k + "\n")
    writeFile(path, "meta_progress_" + num, LINEBREAK)
    writeFile(path, "meta_progress_" + num, "Original Mesh Terms: \n")
    res = []
    seen = set()
    for oriMesh in cleanedOriMeshs:
        obj = next((x for x in MESHINFO if x["term"] == oriMesh or oriMesh in x["entry_list"]), None)
        if obj is not None:
            writeFile(path, "meta_progress_" + num, obj["uid"] + " - " + obj["term"] + "\n")
            seen.add(obj["uid"])
            res.append(obj["term"])
        else:
            suppobj = next((x for x in SUPPINFO if oriMesh in x["names"]), None)
            if suppobj is not None:
                for y in suppobj["ids"]:
                    if y not in seen:
                        obj = next((x for x in MESHINFO if x["uid"] == y), None)
                        if obj is not None:
                            writeFile(path, "meta_progress_" + num, obj["uid"] + " - " + obj["term"] + "\n")
                            res.append(obj["term"])
    writeFile(path, "meta_progress_" + num, LINEBREAK)
    writeFile(path, "meta_progress_" + num, "Generated MeSH Terms: \n")
    for i in objRet:
        writeFile(path, "meta_progress_" + num, i["uid"] + " - " + i["term"] + "\n")
    writeFile(path, "meta_progress_" + num, LINEBREAK)
    return generatedMeshs, objRet, res


def requestMetaMeshs(keywords, num):
    meshs = []
    objs = []
    # seen = set()
    # if num == "one":
    #     for k in keywords:
    #         hashK = hashlib.md5(k.encode())
    #         hashKRes = hashK.hexdigest()
    #         responseF = open("metamap_responses/" + hashKRes, "r")
    #         response = responseF.read()
    #         generatedMeshs, objRet, seen = parseMetaResponse(response, seen, num)
    #         if len(generatedMeshs) is not 0:
    #             for g in generatedMeshs:
    #                 meshs.append(g)
    #         if len(objRet) is not 0:
    #             for i in objRet:
    #                 objs.append(i)
    #     sortedList = sortList(objs)
    #     return meshs, sortedList
    # else:
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
        responseF = open("metamap_responses/" + hashKRes, "r")
        response = responseF.read()
        resContent = json.loads(response)
        if resContent is not None:
            if len(resContent) > 0:
                for item in resContent:
                    score = float(item["CandidateScore"])
                    sources = item["Sources"]
                    if "MSH" in sources and item["CandidatePreferred"] is not None and item["CandidatePreferred"] is not "":
                        temp1 = {
                            "score": float(score) * (-1.00),
                            "term": item["CandidatePreferred"].lower()
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


def sortList(resList):
    if len(resList) > 1:
        scores = []
        for item in resList:
            scores.append(item["score"])
        uniqueScores = list(dict.fromkeys(scores))
        uniqueScores.sort()
        sortedList = []
        grouped = []
        if len(uniqueScores) > 1:
            for score in uniqueScores:
                single = []
                for res in resList:
                    if res["score"] == score:
                        single.append(res)
                grouped.append(single)
            for each in grouped:
                each.sort(key=lambda x: x["uid"])
                for e in each:
                    sortedList.append(e)
            return sortedList
        else:
            return sorted(resList, key=lambda x: x["uid"])
    elif len(resList) == 1:
        return resList
    else:
        return []


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
                # score = score * len(each)
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


# def parseMetaResponse(response, seen, num):
#     generatedMeshs = []
#     generatedMeshObjs = []
#     res = json.loads(response)
#     if res is not None:
#         if num == "one":
#             scores = []
#             for item in res:
#                 scores.append(float(item["CandidateScore"]))
#             if len(scores) > 0:
#                 scores = list(dict.fromkeys(scores))
#                 scores.sort()
#                 selectedScores = scores[0]
#                 for item in res:
#                     score = float(item["CandidateScore"])
#                     if score == selectedScores:
#                         sources = item["Sources"]
#                         if "MSH" in sources and item["CandidatePreferred"] is not None and item["CandidatePreferred"] is not "":
#                             generatedMeshs.append(item["CandidatePreferred"].lower())
#                             temp1 = {
#                                 "term": item["CandidatePreferred"].lower(),
#                                 "score": 1000.00 - (float(score) * (-1.00))
#                             }
#                             generatedMeshObjs.append(temp1)
#             else:
#                 generatedMeshs = []
#         if len(generatedMeshs) > 0:
#             ret = []
#             objRet = []
#             for mesh in generatedMeshObjs:
#                 meshobj = next((x for x in MESHINFO if x["term"] == mesh["term"] or mesh["term"] in x["entry_list"]), None)
#                 if meshobj is not None:
#                     if meshobj["uid"] not in seen:
#                         seen.add(meshobj["uid"])
#                         temp1 = {
#                             "uid": meshobj["uid"],
#                             "term": meshobj["term"],
#                             "score": mesh["score"]
#                         }
#                         objRet.append(temp1)
#                         ret.append(meshobj["term"])
#                 else:
#                     suppobj = next((x for x in SUPPINFO if mesh in x["names"]), None)
#                     if suppobj is not None:
#                         for i in suppobj["ids"]:
#                             if i not in seen:
#                                 seen.add(i)
#                                 obj = next((x for x in MESHINFO if x["uid"] == i), None)
#                                 if obj is not None:
#                                     temp2 = {
#                                         "score": mesh["score"],
#                                         "uid": obj["uid"],
#                                         "term": obj["term"]
#                                     }
#                                     objRet.append(temp2)
#                                     ret.append(obj["term"])
#             if len(ret) > 0:
#                 return cleanTerms(ret), objRet, seen
#             else:
#                 return [], [], seen
#         else:
#             return [], [], seen
#     else:
#         return [], [], seen


def createMetaResFile(path, d, dd, generatedMesh, num):
    resFile = open(path + "/" + "meta_" + num + ".res", "a+")
    count = 1
    for mesh in generatedMesh:
        obj = next((x for x in MESHINFO if x["term"] == mesh["term"] or mesh["term"] in x["entry_list"]), None)
        line = d + "_" + dd + "    " + "0" + "    " + obj["uid"] + "    " + str(
            count) + "    " + str(mesh["score"]) + "    " + path + "\n"
        resFile.write(line)
        count += 1


def generateNewMetaQuery(path, meshs):
    noMeshQF = open(path + "/" + "clause_no_mesh", "r")
    noMeshContent = noMeshQF.read()
    if len(meshs) > 0:
        meshQuery = "[mesh] OR ".join(meshs)
        newQuery = "(" + meshQuery + "[mesh] OR " + noMeshContent[1:]
    else:
        newQuery = noMeshContent
    return newQuery
