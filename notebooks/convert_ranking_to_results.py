
# %%
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
            if topic in qid_mapping:
                topic = qid_mapping[topic]
            r += "{} 0 {} {} {}\n".format(topic, row[1], i, row[2])
    return r


# %%


T = """3 qid:1 1:1 2:1 3:0 4:0.2 5:0 # 1A
2 qid:1 1:0 2:0 3:1 4:0.1 5:1 # 1B
1 qid:1 1:0 2:1 3:0 4:0.4 5:0 # 1C
1 qid:1 1:0 2:0 3:1 4:0.3 5:0 # 1D 
1 qid:2 1:0 2:0 3:1 4:0.2 5:0 # 2A 
2 qid:2 1:1 2:0 3:1 4:0.4 5:0 # 2B
1 qid:2 1:0 2:0 3:1 4:0.1 5:0 # 2C
1 qid:2 1:0 2:0 3:1 4:0.2 5:0 # 2D 
2 qid:3 1:0 2:0 3:1 4:0.1 5:1 # 3A
3 qid:3 1:1 2:1 3:0 4:0.3 5:0 # 3B
4 qid:3 1:1 2:0 3:0 4:0.4 5:1 # 3C
1 qid:3 1:0 2:1 3:1 4:0.5 5:0 # 3D"""

P = """0.059572964077577395
0.41396617153617066
0.8200181715858811
0.2673823849973803
0.33816221817195735
0.9778925739636255
0.18515359061174785
0.4429387416130208
0.6471509484525855
0.028372440907738716
0.029707403686626832
0.9251843781337956"""
