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
         TOTAL_TRAIN_FOLDER_2019, TOTAL_FOLDER_2017, TOTAL_FOLDER_2018, TOTAL_FOLDER_2019]


def main():
    option = input("Select the experiment to run (1. ATM; 2. MetaMap and QuickUMLS): ")
    if option is "1":
        for path in PATHS:
            lineSeperator("#")
            writeFile(path, "atm_progress", "#########################################################\n")
            writeFile(path, "atm_result", "#########################################################\n")
            print("Dataset: " + path)
            writeFile(path, "atm_progress", path + "\n")
            writeFile(path, "atm_result", path + "\n")
            dirs = os.listdir(path)
            totalHits = 0
            totalMeSHs = 0
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
                        writeFile(path, "atm_progress", "*********************************************************\n")
                        # print("Topic: " + d)
                        writeFile(path, "atm_progress", "Topic: " + d + "\n")
                        # print("Sub-Clause Number: " + dd)
                        writeFile(path, "atm_progress", "Sub-Clause Number: " + dd + "\n")
                        # print("Original MeSH Path: " + path + "/" + d + "/" + dd + "/" + "mesh")
                        writeFile(path, "atm_progress", "Original MeSH Path: " + path + "/" + d + "/" + dd + "/" + "mesh" + "\n")
                        # print("Query Path: " + path + "/" + d + "/" + dd + "/" + "clean_clause")
                        writeFile(path, "atm_progress", "Query Path: " + path + "/" + d + "/" + dd + "/" + "clean_clause" + "\n")
                        mesh_f = open(path + "/" + d + "/" + dd + "/" + "mesh", "r")
                        clause_no_mesh_f = open(path + "/" + d + "/" + dd + "/" + "clean_clause", "r")
                        originalMesh = readFile(path, "m", mesh_f)
                        generatedMesh = readFile(path, "c", clause_no_mesh_f)
                        totalMeSHs += len(originalMesh)
                        hits = findMatch(originalMesh, generatedMesh)
                        totalHits += len(hits)
                        # lineSeperator("-")
                        writeFile(path, "atm_progress", "*********************************************************\n")
                        # print("Number of Terms Match: " + str(len(hits)))
                        writeFile(path, "atm_progress", "Number of Terms Match: " + str(len(hits)) + "\n")
                        # print("Correctness: " + str((round(len(hits) / len(originalMesh), 4)) * 100) + "%")
                        writeFile(path, "atm_progress", "Correctness: " + str((round(len(hits) / len(originalMesh), 4)) * 100) + "%" + "\n")
                        writeFile(path, "atm_progress", "*********************************************************\n")
            # lineSeperator("-")
            print("Sub-Clauses Count: " + str(count))
            writeFile(path, "atm_progress", "*********************************************************\n")
            writeFile(path, "atm_result", "*********************************************************\n")
            print("Total Mesh Terms: " + str(totalMeSHs))
            writeFile(path, "atm_progress", "Total Mesh Terms: " + str(totalMeSHs) + "\n")
            writeFile(path, "atm_result", "Total Mesh Terms: " + str(totalMeSHs) + "\n")
            print("Total Matched Terms: " + str(totalHits))
            writeFile(path, "atm_progress", "Total Matched Terms: " + str(totalHits) + "\n")
            writeFile(path, "atm_result", "Total Matched Terms: " + str(totalHits) + "\n")
            print("Overall Correctness: " + str((round(totalHits / totalMeSHs, 4)) * 100) + "%")
            writeFile(path, "atm_progress", "Overall Correctness: " + str((round(totalHits / totalMeSHs, 4)) * 100) + "%" + "\n")
            writeFile(path, "atm_result", "Overall Correctness: " + str((round(totalHits / totalMeSHs, 4)) * 100) + "%" + "\n")
            writeFile(path, "atm_progress", "#########################################################\n")
            writeFile(path, "atm_result", "#########################################################\n")
            lineSeperator("#")
    elif option is "2":
        pass
    else:
        print("Invalid Selection.")


if __name__ == "__main__":
    main()
