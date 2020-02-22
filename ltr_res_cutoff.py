import re

# UMLS Train Res From LTR
UMLS_2017_TRAIN_RES_PATH = "ltr_res/2017/train/2017_ltr_train_umls.res"
UMLS_2018_TRAIN_RES_PATH = "ltr_res/2018/train/2018_ltr_train_umls.res"
UMLS_2019_D_TRAIN_RES_PATH = "ltr_res/2019/train/DTA/2019_ltr_DTA_train_umls.res"
UMLS_2019_I_TRAIN_RES_PATH = "ltr_res/2019/train/Intervention/2019_ltr_Intervention_train_umls.res"

# ATM Train Res From LTR
ATM_2017_TRAIN_RES_PATH = "ltr_res/2017/train/2017_ltr_train_atm.res"
ATM_2018_TRAIN_RES_PATH = "ltr_res/2018/train/2018_ltr_train_atm.res"
ATM_2019_D_TRAIN_RES_PATH = "ltr_res/2019/train/DTA/2019_ltr_DTA_train_atm.res"
ATM_2019_I_TRAIN_RES_PATH = "ltr_res/2019/train/Intervention/2019_ltr_Intervention_train_atm.res"

# METAMAP Train Res From LTR
META_2017_TRAIN_RES_PATH = "ltr_res/2017/train/2017_ltr_train_meta.res"
META_2018_TRAIN_RES_PATH = "ltr_res/2018/train/2018_ltr_train_meta.res"
META_2019_D_TRAIN_RES_PATH = "ltr_res/2019/train/DTA/2019_ltr_DTA_train_meta.res"
META_2019_I_TRAIN_RES_PATH = "ltr_res/2019/train/Intervention/2019_ltr_Intervention_train_meta.res"

# UMLS Test Res From LTR
UMLS_2017_TEST_RES_PATH = "ltr_res/2017/test/2017_ltr_test_umls.res"
UMLS_2018_TEST_RES_PATH = "ltr_res/2018/test/2018_ltr_test_umls.res"
UMLS_2019_D_TEST_RES_PATH = "ltr_res/2019/test/DTA/2019_ltr_DTA_test_umls.res"
UMLS_2019_I_TEST_RES_PATH = "ltr_res/2019/test/Intervention/2019_ltr_Intervention_test_umls.res"

# ATM Test Res From LTR
ATM_2017_TEST_RES_PATH = "ltr_res/2017/test/2017_ltr_test_atm.res"
ATM_2018_TEST_RES_PATH = "ltr_res/2018/test/2018_ltr_test_atm.res"
ATM_2019_D_TEST_RES_PATH = "ltr_res/2019/test/DTA/2019_ltr_DTA_test_atm.res"
ATM_2019_I_TEST_RES_PATH = "ltr_res/2019/test/Intervention/2019_ltr_Intervention_test_atm.res"

# METAMAP Test Res From LTR
META_2017_TEST_RES_PATH = "ltr_res/2017/test/2017_ltr_test_meta.res"
META_2018_TEST_RES_PATH = "ltr_res/2018/test/2018_ltr_test_meta.res"
META_2019_D_TEST_RES_PATH = "ltr_res/2019/test/DTA/2019_ltr_DTA_test_meta.res"
META_2019_I_TEST_RES_PATH = "ltr_res/2019/test/Intervention/2019_ltr_Intervention_test_meta.res"


def main():
    nums = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    # nums = []
    path = UMLS_2017_TEST_RES_PATH
    with open(path, "r") as f:
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
    for each in groupedAll:
        innerAllScores = []
        for m in each:
            innerAllScores.append(float(m["score"]))
        innerMaxScore = max(innerAllScores)
        for n in each:
            n["score"] = innerMaxScore - n["score"]
    for e in groupedAll:
        e.sort(key=lambda y: (y["score"], y["uid"]))
    cutoffGroupedAll = []
    for num in nums:
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
                    if tempScore < eachCutoffScore:
                        tempScore += float(ele["score"])
                        tempGroup.append(ele)
                cutoffGroupedAll.append(tempGroup)
        for k in cutoffGroupedAll:
            k.sort(key=lambda o: (o["score"], o["uid"]))
        splitedPath = path.rsplit('/', 1)
        outPath = splitedPath[0]
        for e in cutoffGroupedAll:
            for ind, innerEle in enumerate(e):
                # Change the file name each run
                f = open(outPath + "/" + "_" + str(int(num)), "a+")
                # Change the last column according to the run
                f.write(innerEle["topic"] + "    0    " + innerEle["uid"] + "    " + str(ind + 1) + "    " + str(innerEle["score"]) + "    " + "2017_umls_test\n")
                f.close()


if __name__ == '__main__':
    main()
