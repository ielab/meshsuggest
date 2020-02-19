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
    return generatedMeshs, res


def requestMetaMeshs(keywords, num):
    meshs = []
    objs = []
    seen = set()
    for k in keywords:
        hashK = hashlib.md5(k.encode())
        hashKRes = hashK.hexdigest()
        responseF = open("metamap_responses/" + hashKRes, "r")
        response = responseF.read()
        generatedMeshs, objRet, seen = parseMetaResponse(response, seen, num)
        if len(generatedMeshs) is not 0:
            for g in generatedMeshs:
                meshs.append(g)
        if len(objRet) is not 0:
            for i in objRet:
                objs.append(i)
    return meshs, objs


def parseMetaResponse(response, seen, num):
    generatedMeshs = []
    res = json.loads(response)
    if res is not None:
        if num == "100":
            for item in res:
                sources = item["Sources"]
                if "MSH" in sources and item["CandidatePreferred"] is not None and item["CandidatePreferred"] is not "":
                    generatedMeshs.append(item["CandidatePreferred"])
        elif num == "1":
            scores = []
            for item in res:
                scores.append(float(item["CandidateScore"]))
            if len(scores) > 0:
                scores = list(dict.fromkeys(scores))
                scores.sort()
                selectedScores = scores[0]
                for item in res:
                    score = float(item["CandidateScore"])
                    if score == selectedScores:
                        sources = item["Sources"]
                        if "MSH" in sources and item["CandidatePreferred"] is not None and item["CandidatePreferred"] is not "":
                            generatedMeshs.append(item["CandidatePreferred"])
            else:
                generatedMeshs = []
        else:
            scores = []
            for item in res:
                scores.append(float(item["CandidateScore"]))
            if len(scores) > 0:
                scores = list(dict.fromkeys(scores))
                totalScore = sum(scores)
                number = float(num)
                percentage = number / 100.00
                for item in res:
                    score = float(item["CandidateScore"])
                    p = float(score / totalScore)
                    if p > percentage:
                        sources = item["Sources"]
                        if "MSH" in sources and item["CandidatePreferred"] is not None and item["CandidatePreferred"] is not "":
                            generatedMeshs.append(item["CandidatePreferred"])
            else:
                generatedMeshs = []
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


def createMetaResFile(path, d, dd, generatedMesh, num):
    resFile = open(path + "/" + "meta_" + num + ".res", "a+")
    count = 1
    for mesh in generatedMesh:
        obj = next((x for x in MESHINFO if x["term"] == mesh or mesh in x["entry_list"]), None)
        line = d + "_" + dd + "    " + "0" + "    " + obj["uid"] + "    " + str(
            count) + "    " + "0.00" + "    " + path + "\n"
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
