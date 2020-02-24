import re
from total_search_eff_res import *


def main():
    for paths in ALL:
        totalContent = []
        for path in paths[:4]:
            content = readAndParseResFile(path)
            filename = path.rsplit("/", 1)[1]
            year = filename.split("_")[0]
            for each in content:
                for element in each:
                    element["topic"] = "{}_{}".format(year, element["topic"])
            totalContent.append(content)
        writeResFile(totalContent, paths[4])


def writeResFile(content, path):
    f = open(path, "w+")
    for each in content:
        for item in each:
            for element in item:
                line = "{topic} 0 {uid} {rank} {score} {desc}\n".format(topic=element["topic"], uid=element["uid"], rank=element["rank"], score=element["score"], desc=element["desc"])
                f.write(line)


def readAndParseResFile(path):
    with open(path, "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    allItems = []
    for each in content:
        splitedLine = re.split(r' +', each)
        oneObj = {
            "topic": splitedLine[0],
            "uid": splitedLine[2],
            "rank": splitedLine[3],
            "score": splitedLine[4],
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


if __name__ == '__main__':
    main()
