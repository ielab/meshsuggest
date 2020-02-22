from ltr_res_100_files import *
import re


def main():
    totalFileCollection = ALL_FILES
    for fileCollection in totalFileCollection:
        ltrResFile = fileCollection[0]
        targetResFile = fileCollection[1]
        groupedLTRResFile = extractResFileAndGroupAll(ltrResFile)
        groupedTargetResFile = extractResFileAndGroupAll(targetResFile)
        uniqueLTRTopic = getUniqueTopics(groupedLTRResFile)
        uniqueTargetTopic = getUniqueTopics(groupedTargetResFile)
        if len(uniqueLTRTopic) != len(uniqueTargetTopic):
            diff = list(set(uniqueTargetTopic) - set(uniqueLTRTopic))
            for ele in diff:
                for itemList in groupedTargetResFile:
                    if itemList[0]["topic"] == ele:
                        newItemList = []
                        for i in itemList:
                            temp = {
                                "topic": i["topic"],
                                "uid": i["uid"],
                                "score": 0.00
                            }
                            newItemList.append(temp)
                        groupedLTRResFile.append(newItemList)
        for g in groupedLTRResFile:
            g.sort(key=lambda x: (x["score"], x["uid"]), reverse=True)
        for el in groupedLTRResFile:
            topic = el[0]["topic"]
            sameTopicInTarget = None
            for lst in groupedTargetResFile:
                if lst[0]["topic"] == topic:
                    sameTopicInTarget = lst
            if len(sameTopicInTarget) != len(el):
                allInnerScores = []
                for k in el:
                    allInnerScores.append(float(k["score"]))
                minInnerScore = min(allInnerScores)
                uniqueLTRUIDs = getUniqueUIDs(el)
                uniqueTargetUIDs = getUniqueUIDs(sameTopicInTarget)
                diffUIDs = list(set(uniqueTargetUIDs) - set(uniqueLTRUIDs))
                for uid in diffUIDs:
                    for rec in sameTopicInTarget:
                        if rec["uid"] == uid:
                            newRec = {
                                "uid": rec["uid"],
                                "topic": rec["topic"],
                                "score": minInnerScore
                            }
                            el.append(newRec)
        for k in groupedLTRResFile:
            k.sort(key=lambda x: (x["score"], x["uid"]), reverse=True)
        for n in groupedLTRResFile:
            for ind, o in enumerate(n):
                line = "{topic} 0 {uid} {ind} {score} {desc}\n".format(topic=o["topic"], uid=o["uid"], ind=ind + 1, score=str(float(o["score"])), desc=fileCollection[3])
                writeLine(fileCollection[2], line)
    print("Done")


def extractResFileAndGroupAll(filePath):
    with open(filePath, "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    allItems = []
    for each in content:
        splitedLine = re.split(r' +', each)
        oneObj = {
            "topic": splitedLine[0],
            "uid": splitedLine[2],
            "score": float(splitedLine[4])
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
        g.sort(key=lambda x: (x["score"], x["uid"]))
    f.close()
    return groupedAll


def getUniqueTopics(grouped):
    allTopics = []
    for ele in grouped:
        allTopics.append(ele[0]["topic"])
    return list(dict.fromkeys(allTopics))


def getUniqueUIDs(lst):
    allUIDs = []
    for ele in lst:
        allUIDs.append(ele["uid"])
    return list(dict.fromkeys(allUIDs))


def writeLine(path, data):
    f = open(path, "a+")
    f.write(data)
    f.close()


if __name__ == '__main__':
    main()
