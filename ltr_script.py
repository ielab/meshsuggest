import subprocess

quickrank_path = "/Users/summerfrogman/ielab/quickrank/bin/quicklearn"


def main():
    print("1. Train")
    print("2. Test")
    option = input()
    if option == "1":
        algo = "LAMBDAMART"
        metric = "NDCG"
        trainFeatures = [
            "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/2017_ATM_train_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/2018_ATM_train_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/2019_ATM_D_train_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/2019_ATM_I_train_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/2017_Meta_train_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/2018_Meta_train_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/2019_Meta_D_train_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/2019_Meta_I_train_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/2017_UMLS_train_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/2018_UMLS_train_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/2019_UMLS_D_train_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_trains/2019_UMLS_I_train_features.features"
        ]
        modelOutPath = "/Users/summerfrogman/ielab/meshsuggest/ltr_models"
        trainSets = []
        for num in range(12):
            if num < 4:
                oneSet = {
                    "feature": trainFeatures[num],
                    "name": "ATM"
                }
                trainSets.append(oneSet)
            elif 8 > num >= 4:
                oneSet = {
                    "feature": trainFeatures[num],
                    "name": "Meta"
                }
                trainSets.append(oneSet)
            elif num >= 8:
                oneSet = {
                    "feature": trainFeatures[num],
                    "name": "UMLS"
                }
                trainSets.append(oneSet)
        for ind, item in enumerate(trainSets):
            if ind == 0 or ind == 4 or ind == 8:
                year = "2017"
            elif ind == 1 or ind == 5 or ind == 9:
                year = "2018"
            else:
                year = "2019"
            if ind == 2 or ind == 6 or ind == 10:
                subset = "D"
            elif ind == 3 or ind == 7 or ind == 11:
                subset = "I"
            else:
                subset = ""
            if subset is not "":
                modelFileName = '{modelOutPath}/{year}_{metric}_{model}_{subset}_model.xml'.format(modelOutPath=modelOutPath, year=year, metric=metric, model=item["name"], subset=subset)
            else:
                modelFileName = '{modelOutPath}/{year}_{metric}_{model}_model.xml'.format(modelOutPath=modelOutPath, year=year, metric=metric, model=item["name"])
            queryTrainParam = ' --algo {algo} ' \
                              '--features {featureFile} ' \
                              '--train-metric {metric} ' \
                              '--model-out {modelOutPath}'.format(algo=algo, featureFile=item["feature"], metric=metric, modelOutPath=modelFileName)
            print(quickrank_path + queryTrainParam)
            subprocess.call(quickrank_path + queryTrainParam, shell=True)
        print("Training Done.")
    if option == "2":
        scoreOutPath = "/Users/summerfrogman/ielab/meshsuggest/ltr_scores"
        metric = "NDCG"
        testFeatureFiles = [
            "/Users/summerfrogman/ielab/meshsuggest/ltr_tests/2017_ATM_test_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_tests/2018_ATM_test_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_tests/2019_ATM_D_test_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_tests/2019_ATM_I_test_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_tests/2017_Meta_test_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_tests/2018_Meta_test_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_tests/2019_Meta_D_test_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_tests/2019_Meta_I_test_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_tests/2017_UMLS_test_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_tests/2018_UMLS_test_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_tests/2019_UMLS_D_test_features.features",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_tests/2019_UMLS_I_test_features.features"
        ]
        modelsPath = [
            "/Users/summerfrogman/ielab/meshsuggest/ltr_models/2017_NDCG_ATM_model.xml",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_models/2018_NDCG_ATM_model.xml",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_models/2019_NDCG_ATM_D_model.xml",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_models/2019_NDCG_ATM_I_model.xml",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_models/2017_NDCG_Meta_model.xml",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_models/2018_NDCG_Meta_model.xml",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_models/2019_NDCG_Meta_D_model.xml",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_models/2019_NDCG_Meta_I_model.xml",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_models/2017_NDCG_UMLS_model.xml",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_models/2018_NDCG_UMLS_model.xml",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_models/2019_NDCG_UMLS_D_model.xml",
            "/Users/summerfrogman/ielab/meshsuggest/ltr_models/2019_NDCG_UMLS_I_model.xml"
        ]
        testSets = []
        for num in range(12):
            if num < 4:
                oneSet = {
                    "model": modelsPath[num],
                    "featureFile": testFeatureFiles[num],
                    "name": "ATM"
                }
                testSets.append(oneSet)
            elif 8 > num >= 4:
                oneSet = {
                    "model": modelsPath[num],
                    "featureFile": testFeatureFiles[num],
                    "name": "Meta"
                }
                testSets.append(oneSet)
            elif num >= 8:
                oneSet = {
                    "model": modelsPath[num],
                    "featureFile": testFeatureFiles[num],
                    "name": "UMLS"
                }
                testSets.append(oneSet)
        for ind, item in enumerate(testSets):
            if ind == 0 or ind == 4 or ind == 8:
                year = "2017"
            elif ind == 1 or ind == 5 or ind == 9:
                year = "2018"
            else:
                year = "2019"
            if ind == 2 or ind == 6 or ind == 10:
                subset = "D"
            elif ind == 3 or ind == 7 or ind == 11:
                subset = "I"
            else:
                subset = ""
            if subset is not "":
                scoreFileName = '{scoreOutPath}/{year}_{metric}_{model}_{subset}_score.txt'.format(scoreOutPath=scoreOutPath, year=year, metric=metric, model=item["name"], subset=subset)
            else:
                scoreFileName = '{scoreOutPath}/{year}_{metric}_{model}_score.txt'.format(scoreOutPath=scoreOutPath, year=year, metric=metric, model=item["name"])
            queryTestParam = ' --features {featureFile} ' \
                             '--model-in {modelInput} ' \
                             '--test-metric {metric} ' \
                             '--scores {scoreFileName}'.format(featureFile=item["featureFile"], metric=metric, modelInput=item["model"], scoreFileName=scoreFileName)
            subprocess.call(quickrank_path + queryTestParam, shell=True)
        print("Testing Done.")


if __name__ == "__main__":
    main()
