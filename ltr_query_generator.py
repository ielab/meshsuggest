import os
import re


def main():
    filenames = os.listdir("/Users/summerfrogman/ielab/meshsuggest/ltr_res/test/cutoffs")
    trash = ".DS_Store"
    if trash in filenames:
        filenames.remove(trash)
    for filename in filenames:
        grouped = readAndParseResFile(filename)
        print(grouped)


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
            "uid": splitedLine[2]
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
