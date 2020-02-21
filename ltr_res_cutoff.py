import re

# UMLS Train Res From LTR
UMLS_2017_TRAIN_RES_PATH = "ltr_res/2017/train/umls.res"
UMLS_2018_TRAIN_RES_PATH = "ltr_res/2018/train/umls.res"
UMLS_2019_D_TRAIN_RES_PATH = "ltr_res/2019/train/DTA/umls.res"
UMLS_2019_I_TRAIN_RES_PATH = "ltr_res/2019/train/Intervention/umls.res"

# ATM Train Res From LTR
ATM_2017_TRAIN_RES_PATH = "ltr_res/2017/train/atm.res"
ATM_2018_TRAIN_RES_PATH = "ltr_res/2018/train/atm.res"
ATM_2019_D_TRAIN_RES_PATH = "ltr_res/2019/train/DTA/atm.res"
ATM_2019_I_TRAIN_RES_PATH = "ltr_res/2019/train/Intervention/atm.res"

# METAMAP Train Res From LTR
META_2017_TRAIN_RES_PATH = "ltr_res/2017/train/meta.res"
META_2018_TRAIN_RES_PATH = "ltr_res/2018/train/meta.res"
META_2019_D_TRAIN_RES_PATH = "ltr_res/2019/train/DTA/meta.res"
META_2019_I_TRAIN_RES_PATH = "ltr_res/2019/train/Intervention/meta.res"

# UMLS Test Res From LTR
UMLS_2017_TEST_RES_PATH = "ltr_res/2017/test/umls.res"
UMLS_2018_TEST_RES_PATH = "ltr_res/2018/test/umls.res"
UMLS_2019_D_TEST_RES_PATH = "ltr_res/2019/test/DTA/umls.res"
UMLS_2019_I_TEST_RES_PATH = "ltr_res/2019/test/Intervention/umls.res"

# ATM Test Res From LTR
ATM_2017_TEST_RES_PATH = "ltr_res/2017/test/atm.res"
ATM_2018_TEST_RES_PATH = "ltr_res/2018/test/atm.res"
ATM_2019_D_TEST_RES_PATH = "ltr_res/2019/test/DTA/atm.res"
ATM_2019_I_TEST_RES_PATH = "ltr_res/2019/test/Intervention/atm.res"

# METAMAP Test Res From LTR
META_2017_TEST_RES_PATH = "ltr_res/2017/test/meta.res"
META_2018_TEST_RES_PATH = "ltr_res/2018/test/meta.res"
META_2019_D_TEST_RES_PATH = "ltr_res/2019/test/DTA/meta.res"
META_2019_I_TEST_RES_PATH = "ltr_res/2019/test/Intervention/meta.res"


def main():
    num = input("Cut off: ")
    num = int(num)
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


if __name__ == '__main__':
    main()
