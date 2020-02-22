import re


def main():
    lookupPath = "/Users/summerfrogman/ielab/meshsuggest/ltr_lookup/2019_training_Intervention.lookup"
    scoreFilePath = "/Users/summerfrogman/ielab/meshsuggest/ltr_scores/train/2019_NDCG_ATM_I_score.txt"
    featureFilePath = "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/norm/2019_ATM_I_train_norm.features"
    resOutPath = "/Users/summerfrogman/ielab/meshsuggest/ltr_res/train/2019_ATM_I_train.res"
    scoreFile = open(scoreFilePath, "r")
    scoreFileContent = scoreFile.read()
    featureFile = open(featureFilePath, "r")
    featureFileContent = featureFile.read()
    lookupMap = get_qid_mapping(lookupPath)
    res = convert_predictions_and_features(featureFileContent, scoreFileContent, lookupMap)
    resFile = open(resOutPath, "w+")
    resFile.write(res)
    print("Done")


def get_qid_mapping(loopup_path):
    qid_mapping = {}
    with open(loopup_path, "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for each in content:
        splitedLine = re.split(r' +', each)
        qid_mapping[int(splitedLine[1])] = splitedLine[0]
    return qid_mapping


def split_predictions_and_features(features: [], predictions: []):
    f = {}
    for i, feature in enumerate(features):
        qid = feature[0]
        if qid not in f:
            f[qid] = []
        f[qid].append((predictions[i], feature[1]))
    for k, v in f.items():
        yield [(k, x[0][1], x[0][0]) for x in reversed(sorted(zip(v)))]


def sort_predictions_and_features(features: str, predictions: str) -> []:
    f = [(int(x.split(" ")[1].strip().split(":")[-1]), x.split("#")[-1].strip()) for x in features.split("\n")]
    p = [float(x) for x in predictions.split("\n")]
    return list(split_predictions_and_features(f, p))


def convert_predictions_and_features(features: str, predictions: str, qid_mapping: dict) -> str:
    r = ""
    s = sort_predictions_and_features(features, predictions)
    for X in s:
        for i, row in enumerate(X):
            topic = row[0]
            if topic in qid_mapping.keys():
                topic = qid_mapping[topic]
            r += "{} 0 {} {} {} 2017_NDCG_ATM\n".format(topic, row[1], i+1, row[2])
    return r


if __name__ == '__main__':
    main()
