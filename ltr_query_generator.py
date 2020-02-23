import os
import re
import json
import collections

MESHINFOF = open("mesh.json", "r")
MESHINFO = json.loads(MESHINFOF.read())
MESHINFOF.close()

PATH_PREFIX = "/Users/summerfrogman/ielab/meshsuggest/data/clef_tar_processed"


def main():
    filenames = os.listdir("/Users/summerfrogman/ielab/meshsuggest/ltr_res/test/cutoffs")
    trash = ".DS_Store"
    if trash in filenames:
        filenames.remove(trash)
    for filename in filenames:
        grouped = readAndParseResFile(filename)
        print("Processing File: {}".format(filename))
        originalDataPath = ""
        desc = grouped[0][0]["desc"]
        splitedDesc = desc.split("_")
        year = splitedDesc[0]
        method = splitedDesc[1].lower()
        if year == "2019":
            subCategory = splitedDesc[2]
            if subCategory == "I":
                originalDataPath = "{}/{}/testing/{}".format(PATH_PREFIX, year, "Intervention")
            elif subCategory == "D":
                originalDataPath = "{}/{}/testing/{}".format(PATH_PREFIX, year, "DTA")
        else:
            originalDataPath = "{}/{}/testing".format(PATH_PREFIX, year)
        completeTopics = getCompleteTopicList(originalDataPath)
        ltrTopicAndMesh = getLTRTopicsAndMeSH(grouped)
        ltrTopicAndMesh = compareAndAddMissingTopic(originalDataPath, completeTopics, ltrTopicAndMesh)
        ltrTopicAndMesh = compareAndAddMissingSub(originalDataPath, ltrTopicAndMesh)
        produceLTRQuery(ltrTopicAndMesh, method, originalDataPath)


def produceLTRQuery(ltrTopics, method, path):
    topic = list(ltrTopics.keys())
    for t in topic:
        print("Topic: {}".format(t))
        query = constructLTRQuery(t, ltrTopics, path)
        writeQueryFile(query, t, path, method)


def writeQueryFile(query, t, path, method):
    queryOutPath = "{}/{}/ltr_{}_result_query".format(path, t, method.lower())
    f = open(queryOutPath, "w+")
    f.write(query)
    f.close()


def constructLTRQuery(topic, ltrTopics, path):
    allSubs = ltrTopics[topic]
    allSubKeys = []
    for each in allSubs:
        allSubKeys += list(each.keys())
    queryFragmentsList = []
    for key in allSubKeys:
        newPath = "{}/{}/{}".format(path, topic, key)
        cleanQuery = getCleanQuery(newPath)
        if len(allSubs[int(key)-1][key]) > 0:
            meshTerms = allSubs[int(key)-1][key]
            meshQuery = "[mesh] OR ".join(meshTerms)
            newQuery = "(" + meshQuery + "[mesh] OR " + cleanQuery[1:]
            queryFragmentsList.append(newQuery)
        else:
            queryFragmentsList.append(cleanQuery)
    return " AND ".join(queryFragmentsList)


def compareAndAddMissingSub(originalDataPath, ltrTopics):
    topics = list(ltrTopics.keys())
    for each in topics:
        subs = getCompleteTopicList("{}/{}".format(originalDataPath, each))
        ltrSubsList = ltrTopics[each]
        ltrSubs = []
        for item in ltrSubsList:
            ltrSubs += item.keys()
        diff = list(set(subs) - set(ltrSubs))
        if len(diff) > 0:
            for sub in diff:
                temp = {
                    sub: []
                }
                ltrTopics[each].append(temp)
    for k in topics:
        ltrTopics[k].sort(key=getKey)
    return ltrTopics


def getKey(item):
    keys = list(item.keys())
    key = keys[0]
    return key


def compareAndAddMissingTopic(originalDataPath, completeTopics, ltrTopics):
    diff = list(set(completeTopics) - set(ltrTopics.keys()))
    if len(diff) > 0:
        for each in diff:
            subs = getCompleteTopicList("{}/{}".format(originalDataPath, each))
            subList = []
            for s in subs:
                temp = {
                    s: []
                }
                subList.append(temp)
            ltrTopics[each] = subList
    orderedLTRTopics = collections.OrderedDict(sorted(ltrTopics.items()))
    return orderedLTRTopics


def readAndParseResFile(filename):
    path = "/Users/summerfrogman/ielab/meshsuggest/ltr_res/test/cutoffs/{}".format(filename)
    with open(path, "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    allItems = []
    for each in content:
        splitedLine = re.split(r' +', each)
        oneObj = {
            "topic": splitedLine[0],
            "uid": splitedLine[2],
            "desc": splitedLine[5]
        }
        allItems.append(oneObj)
    topics = []
    for item in allItems:
        topics.append(item["topic"])
    uniqueTopics = list(dict.fromkeys(topics))
    uniqueTopics.sort()
    groupedAll = []
    for topic in uniqueTopics:
        grouped = []
        for t in allItems:
            if t["topic"] == topic:
                grouped.append(t)
            else:
                continue
        if len(grouped) > 0:
            groupedAll.append(grouped)
    for g in groupedAll:
        g.sort(key=lambda x: x["uid"])
    return groupedAll


def getCleanQuery(path):
    newPath = "{}/clause_no_mesh".format(path)
    f = open(newPath, "r")
    cleanQuery = f.read()
    return cleanQuery


def getCompleteTopicList(path):
    lst = [dI for dI in os.listdir(path) if os.path.isdir(os.path.join(path, dI))]
    lst.sort()
    return lst


def getLTRTopicsAndMeSH(grouped):
    ltrTopics = {}
    tempTopics = []
    for each in grouped:
        topic = each[0]["topic"].split("_")[0]
        tempTopics.append(topic)
    uniqueTopics = list(dict.fromkeys(tempTopics))
    for t in uniqueTopics:
        temp = []
        for ele in grouped:
            if t in ele[0]["topic"]:
                for i in ele:
                    temp.append(i["topic"].split("_")[1])
        temp = list(dict.fromkeys(temp))
        ltrTopics[t] = temp
    for top in uniqueTopics:
        subList = ltrTopics[top]
        meshSubObj = []
        for eve in subList:
            lowerTopic = "{}_{}".format(top, eve)
            mesh = []
            for i in grouped:
                if i[0]["topic"] == lowerTopic:
                    for k in i:
                        mesh.append(getSubTopicMeSHTerms(k["uid"]))
            topicMeshObj = {eve: mesh}
            meshSubObj.append(topicMeshObj)
        ltrTopics[top] = meshSubObj
    return ltrTopics


def getSubTopicMeSHTerms(uid):
    mesh = None
    for item in MESHINFO:
        if item["uid"] == uid:
            mesh = item["term"]
    return mesh


if __name__ == '__main__':
    main()
