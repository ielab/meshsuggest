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

# TEST
TEST = "test"

PATHS = [TEST_FOLDER_2017, TRAIN_FOLDER_2017, TEST_FOLDER_2018, TRAIN_FOLDER_2018, TEST_DTA_FOLDER_2019,
         TEST_INTERVENTION_FOLDER_2019, TOTAL_TEST_FOLDER_2019, TRAIN_DTA_FOLDER_2019, TRAIN_INTERVENTION_FOLDER_2019,
         TOTAL_TRAIN_FOLDER_2019, TOTAL_FOLDER_2017, TOTAL_FOLDER_2018, TOTAL_FOLDER_2019, TOTAL_DATASET]


def main():
    option = input("Select the experiment to run (1. ATM; 2. MetaMap and QuickUMLS): ")
    if option is "1":
        for path in PATHS:
            lineSeperator("=")
            writeFile(path, "atm_progress", "=========================================================\n")
            writeFile(path, "atm_result", "=========================================================\n")
            print("Dataset: " + path)
            writeFile(path, "atm_progress", path + "\n")
            writeFile(path, "atm_result", path + "\n")
            dirs = os.listdir(path)
            totalHits = 0
            totalMeSHs = 0
            totalGen = 0
            count = 0
            printProgressBar(0, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
            for i, d in enumerate(dirs):
                printProgressBar(i + 1, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
                if d is not ".DS_Store" and os.path.isdir(path + "/" + d):
                    innerD = os.listdir(path + "/" + d)
                    if ".DS_Store" in innerD:
                        innerD.remove(".DS_Store")
                        count += len(innerD)
                    for dd in innerD:
                        # lineSeperator("-")
                        writeFile(path, "atm_progress", "---------------------------------------------------------\n")
                        # print("Topic: " + d)
                        writeFile(path, "atm_progress", "Topic: " + d + "\n")
                        # print("Sub-Clause Number: " + dd)
                        writeFile(path, "atm_progress", "Sub-Clause: " + dd + "\n")
                        # print("Original MeSH Path: " + path + "/" + d + "/" + dd + "/" + "mesh")
                        writeFile(path, "atm_progress", "Original MeSH Path: " + path + "/" + d + "/" + dd + "/" + "mesh" + "\n")
                        # print("Query Path: " + path + "/" + d + "/" + dd + "/" + "clean_clause")
                        writeFile(path, "atm_progress", "Cleaned Query Path: " + path + "/" + d + "/" + dd + "/" + "clean_clause" + "\n")
                        meshF = open(path + "/" + d + "/" + dd + "/" + "mesh", "r")
                        clauseNoMeshF = open(path + "/" + d + "/" + dd + "/" + "clean_clause", "r")
                        originalMesh = readFile(path, "m", meshF)
                        generatedMesh = readFile(path, "c", clauseNoMeshF)
                        hits = findMatch(originalMesh, generatedMesh)
                        totalMeSHs += len(originalMesh)
                        totalGen += len(generatedMesh)
                        totalHits += len(hits)
                        # lineSeperator("-")
                        writeFile(path, "atm_progress", "---------------------------------------------------------\n")
                        # print("Number of Original MeSH Terms: " + str(len(originalMesh)))
                        writeFile(path, "atm_progress", "Number of Original MeSH Terms: " + str(len(originalMesh)) + "\n")
                        # print("Number of ATM Generated MeSH Terms: " + str(len(generatedMesh)))
                        writeFile(path, "atm_progress", "Number of ATM Generated MeSH Terms: " + str(len(generatedMesh)) + "\n")
                        # print("Number of Terms Matched: " + str(len(hits)))
                        writeFile(path, "atm_progress", "Number of Terms Matched: " + str(len(hits)) + "\n")
                        # print("Recall: " + str((round(len(hits) / len(originalMesh), 4)) * 100) + "%")
                        writeFile(path, "atm_progress", "Recall: " + str((round(len(hits) / len(originalMesh), 4)) * 100) + "%" + "\n")
                        if len(generatedMesh) is 0:
                            pre = 0
                        else:
                            pre = (round(len(hits) / len(generatedMesh), 4)) * 100
                        # print("Precision: " + str(pre) + "%")
                        writeFile(path, "atm_progress", "Precision: " + str(pre) + "%" + "\n")
                        # lineSeperator("-")
                        writeFile(path, "atm_progress", "---------------------------------------------------------\n")
            # lineSeperator("-")
            writeFile(path, "atm_progress", "---------------------------------------------------------\n")
            writeFile(path, "atm_result", "---------------------------------------------------------\n")
            print("Total Sub-Clauses: " + str(count))
            writeFile(path, "atm_progress", "Total Sub-Clauses: " + str(count) + "\n")
            writeFile(path, "atm_result", "Total Sub-Clauses: " + str(count) + "\n")
            print("Total Original MeSH Terms: " + str(totalMeSHs))
            writeFile(path, "atm_progress", "Total Original MeSH Terms: " + str(totalMeSHs) + "\n")
            writeFile(path, "atm_result", "Total Original MeSH Terms: " + str(totalMeSHs) + "\n")
            print("Total Generated MeSH Terms: " + str(totalGen))
            writeFile(path, "atm_progress", "Total Generated MeSH Terms: " + str(totalGen) + "\n")
            writeFile(path, "atm_result", "Total Generated MeSH Terms: " + str(totalGen) + "\n")
            print("Total Matched MeSH Terms: " + str(totalHits))
            writeFile(path, "atm_progress", "Total Matched MeSH Terms: " + str(totalHits) + "\n")
            writeFile(path, "atm_result", "Total Matched MeSH Terms: " + str(totalHits) + "\n")
            print("Overall Recall: " + str((round(totalHits / totalMeSHs, 4)) * 100) + "%")
            writeFile(path, "atm_progress", "Overall Recall: " + str((round(totalHits / totalMeSHs, 4)) * 100) + "%" + "\n")
            writeFile(path, "atm_result", "Overall Recall: " + str((round(totalHits / totalMeSHs, 4)) * 100) + "%" + "\n")
            if totalGen is 0:
                opre = 0
            else:
                opre = (round(totalHits / totalGen, 4)) * 100
            print("Overall Precision: " + str(opre) + "%")
            writeFile(path, "atm_progress", "Overall Precision: " + str((round(totalHits / totalGen, 4)) * 100) + "%" + "\n")
            writeFile(path, "atm_result", "Overall Precision: " + str((round(totalHits / totalGen, 4)) * 100) + "%" + "\n")
            writeFile(path, "atm_progress", "=========================================================\n")
            writeFile(path, "atm_result", "=========================================================\n")
            lineSeperator("=")
    elif option is "2":
        pass
    else:
        print("Invalid Selection.")


if __name__ == "__main__":
    main()
