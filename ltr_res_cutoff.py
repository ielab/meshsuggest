import re
from ltr_cutoff_res_files import *


def main():
    nums = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    # nums = [50]
    # nums = [1]
    for path in TRAIN_PATHS:
        with open(path[0], "r") as f:
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
        for member in groupedAll:
            allMemberScores = []
            for innerMember in member:
                allMemberScores.append(float(innerMember["score"]))
            memberMaxScore = max(allMemberScores)
            memberMinScore = min(allMemberScores)
            for innerMember in member:
                if memberMaxScore != memberMinScore:
                    innerMember["score"] = (float(innerMember["score"]) - memberMinScore) / (memberMaxScore - memberMinScore)
                else:
                    innerMember["score"] = 1.00
        for each in groupedAll:
            innerAllScores = []
            for m in each:
                innerAllScores.append(float(m["score"]))
            innerMaxScore = max(innerAllScores)
            for n in each:
                n["score"] = innerMaxScore - n["score"]
        for e in groupedAll:
            e.sort(key=lambda y: (y["score"], y["uid"]))
        for num in nums:
            cutoffGroupedAll = []
            num = float(num)
            for c in groupedAll:
                eachCutoffTotalScore = 0.0
                for ele in c:
                    eachCutoffTotalScore += ele["score"]
                if eachCutoffTotalScore == 0.0:
                    cutoffGroupedAll.append(c)
                else:
                    eachCutoffScore = eachCutoffTotalScore * (num / 100.0)
                    tempScore = 0.0
                    tempGroup = []
                    for ele in c:
                        if (tempScore + float(ele["score"])) <= eachCutoffScore:
                            tempScore += float(ele["score"])
                            tempGroup.append(ele)
                        else:
                            break
                    cutoffGroupedAll.append(tempGroup)
            for k in cutoffGroupedAll:
                k.sort(key=lambda o: (o["score"], o["uid"]))
            for e in cutoffGroupedAll:
                for ind, innerEle in enumerate(e):
                    desc = "{d}_{n}".format(d=path[2], n=int(num))
                    line = "{topic} 0 {uid} {ind} {score} {desc}\n".format(topic=innerEle["topic"], uid=innerEle["uid"],
                                                                           ind=ind + 1,
                                                                           score=float(innerEle["score"]),
                                                                           desc=desc)
                    outPath = "{pathPrefix}_{num}.res".format(pathPrefix=path[1], num=int(num))
                    f = open(outPath, "a+")
                    f.write(line)
                    f.close()


if __name__ == '__main__':
    main()
