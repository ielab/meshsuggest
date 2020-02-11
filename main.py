from helper import *
import os

# 2017 DATASET
TEST_FOLDER_2017 = "data/clef_tar_processed/2017/testing"
TRAIN_FOLDER_2017 = "data/clef_tar_processed/2017/training"
TOTAL_FOLDER_2017 = "data/clef_tar_processed/2017/total"

# 2018 DATASET
TEST_FOLDER_2018 = "data/clef_tar_processed/2018/testing"
TRAIN_FOLDER_2018 = "data/clef_tar_processed/2018/training"
TOTAL_FOLDER_2018 = "data/clef_tar_processed/2018/total"

# 2019 DATASET
TEST_DTA_FOLDER_2019 = "data/clef_tar_processed/2019/testing/DTA"
TEST_INTERVENTION_FOLDER_2019 = "data/clef_tar_processed/2019/testing/Intervention"
TOTAL_TEST_FOLDER_2019 = "data/clef_tar_processed/2019/testing/total"
TRAIN_DTA_FOLDER_2019 = "data/clef_tar_processed/2019/training/DTA"
TRAIN_INTERVENTION_FOLDER_2019 = "data/clef_tar_processed/2019/training/Intervention"
TOTAL_TRAIN_FOLDER_2019 = "data/clef_tar_processed/2019/training/total"
TOTAL_FOLDER_2019 = "data/clef_tar_processed/2019/total"

# TOTAL DATASET
TOTAL_DATASET = "data/clef_tar_processed/total"

PATHS = [TEST_FOLDER_2017, TRAIN_FOLDER_2017, TEST_FOLDER_2018, TRAIN_FOLDER_2018, TEST_DTA_FOLDER_2019,
         TEST_INTERVENTION_FOLDER_2019, TOTAL_TEST_FOLDER_2019, TRAIN_DTA_FOLDER_2019, TRAIN_INTERVENTION_FOLDER_2019,
         TOTAL_TRAIN_FOLDER_2019, TOTAL_FOLDER_2017, TOTAL_FOLDER_2018, TOTAL_FOLDER_2019]


def main():
    for path in PATHS:
        lineSeperator("#")
        print("Dataset: " + path)
        dirs = os.listdir(path)
        totalHits = 0
        totalMeSHs = 0
        printProgressBar(0, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
        for i, d in enumerate(dirs):
            printProgressBar(i + 1, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
            if d is not ".DS_Store" and os.path.isdir(path + "/" + d):
                innerD = os.listdir(path + "/" + d)
                if ".DS_Store" in innerD:
                    innerD.remove(".DS_Store")
                for dd in innerD:
                    # lineSeperator("-")
                    # print("Topic: " + d)
                    # print("Sub-Clause Number: " + dd)
                    # print("Original MeSH Path: " + path + "/" + d + "/" + dd + "/" + "mesh")
                    # print("Query Path: " + path + "/" + d + "/" + dd + "/" + "clean_clause")
                    mesh_f = open(path + "/" + d + "/" + dd + "/" + "mesh", "r")
                    clause_no_mesh_f = open(path + "/" + d + "/" + dd + "/" + "clean_clause", "r")
                    originalMesh = readFile("m", mesh_f)
                    generatedMesh = readFile("c", clause_no_mesh_f)
                    totalMeSHs += len(originalMesh)
                    hits = findMatch(originalMesh, generatedMesh)
                    totalHits += len(hits)
                    # lineSeperator("-")
                    # print("Number of Terms Match: " + str(len(hits)))
                    # print("Correctness: " + str((round(len(hits) / len(originalMesh), 4)) * 100) + "%")
        # lineSeperator("-")
        print("Total Mesh Terms: " + str(totalMeSHs))
        print("Total Matched Terms: " + str(totalHits))
        print("Overall Correctness: " + str((round(totalHits / totalMeSHs, 4)) * 100) + "%")
        lineSeperator("#")


if __name__ == "__main__":
    main()
