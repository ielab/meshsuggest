from atm_helper import *
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

ENDBLOCK = "=========================================================\n"

PATHS = [TEST_FOLDER_2017, TRAIN_FOLDER_2017,
         TOTAL_FOLDER_2017, TEST_FOLDER_2018, TRAIN_FOLDER_2018,
         TOTAL_FOLDER_2018, TEST_DTA_FOLDER_2019, TEST_INTERVENTION_FOLDER_2019, TOTAL_TEST_FOLDER_2019,
         TRAIN_DTA_FOLDER_2019, TRAIN_INTERVENTION_FOLDER_2019, TOTAL_TRAIN_FOLDER_2019,
         TOTAL_FOLDER_2019,
         TOTAL_DATASET]

TEST = ["test"]


def main():
    print("1. ATM")
    print("2. MetaMap")
    print("3. UMLS")
    print("4. Generate qrels and result file for ATM")
    print("5. Generate res file for MetaMap")
    print("6. Generate res file for UMLS")
    print("7. Entity Retrieval")
    option = input("Selection: ")
    if option is "1":
        for path in PATHS:
            lineSeperator("=")
            writeFile(path, "atm_progress", ENDBLOCK)
            writeFile(path, "atm_result", ENDBLOCK)
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
                    fullNewATMQuery = ""
                    fullOriginalQuery = ""
                    for dd in innerD:
                        writeFile(path, "atm_progress", LINEBREAK)
                        writeFile(path, "atm_progress", "Topic: " + d + "\n")
                        writeFile(path, "atm_progress", "Sub-Clause: " + dd + "\n")
                        writeFile(path, "atm_progress",
                                  "Original MeSH Path: " + path + "/" + d + "/" + dd + "/" + "mesh" + "\n")
                        writeFile(path, "atm_progress",
                                  "Cleaned Query Path: " + path + "/" + d + "/" + dd + "/" + "clean_clause" + "\n")
                        meshF = open(path + "/" + d + "/" + dd + "/" + "mesh", "r")
                        clauseNoMeshF = open(path + "/" + d + "/" + dd + "/" + "clean_clause", "r")
                        originalMesh = readFile(path, "m", meshF)
                        generatedMesh, cleaned = readFile(path, "c", clauseNoMeshF)
                        newQuery = generateNewQuery(path + "/" + d + "/" + dd, cleaned)
                        if fullNewATMQuery is "":
                            fullNewATMQuery = newQuery
                        else:
                            fullNewATMQuery = fullNewATMQuery + " AND " + newQuery
                        originalQuery = getOriginalQuery(path + "/" + d + "/" + dd)
                        if fullOriginalQuery is "":
                            fullOriginalQuery = originalQuery
                        else:
                            fullOriginalQuery = fullOriginalQuery + " AND " + originalQuery
                        hits = findMatch(originalMesh, generatedMesh)
                        totalMeSHs += len(originalMesh)
                        totalGen += len(generatedMesh)
                        totalHits += len(hits)
                        writeFile(path, "atm_progress", LINEBREAK)
                        writeFile(path, "atm_progress",
                                  "Number of Original MeSH Terms: " + str(len(originalMesh)) + "\n")
                        writeFile(path, "atm_progress",
                                  "Number of ATM Generated MeSH Terms: " + str(len(generatedMesh)) + "\n")
                        writeFile(path, "atm_progress", "Number of Terms Matched: " + str(len(hits)) + "\n")
                        writeFile(path, "atm_progress",
                                  "Recall: " + str((round(len(hits) / len(originalMesh), 4)) * 100) + "%" + "\n")
                        if len(generatedMesh) is 0:
                            pre = 0
                        else:
                            pre = (round(len(hits) / len(generatedMesh), 4)) * 100
                        writeFile(path, "atm_progress", "Precision: " + str(pre) + "%" + "\n")
                        writeFile(path, "atm_progress", LINEBREAK)
                    writeFile(path + "/" + d, "atm_result_query", fullNewATMQuery)
                    writeFile(path + "/" + d, "original_full_query", fullOriginalQuery)
            writeFile(path, "atm_progress", LINEBREAK)
            writeFile(path, "atm_result", LINEBREAK)
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
            writeFile(path, "atm_progress",
                      "Overall Recall: " + str((round(totalHits / totalMeSHs, 4)) * 100) + "%" + "\n")
            writeFile(path, "atm_result",
                      "Overall Recall: " + str((round(totalHits / totalMeSHs, 4)) * 100) + "%" + "\n")
            if totalGen is 0:
                opre = 0
            else:
                opre = (round(totalHits / totalGen, 4)) * 100
            print("Overall Precision: " + str(opre) + "%")
            writeFile(path, "atm_progress",
                      "Overall Precision: " + str((round(totalHits / totalGen, 4)) * 100) + "%" + "\n")
            writeFile(path, "atm_result",
                      "Overall Precision: " + str((round(totalHits / totalGen, 4)) * 100) + "%" + "\n")
            writeFile(path, "atm_progress", ENDBLOCK)
            writeFile(path, "atm_result", ENDBLOCK)
            lineSeperator("=")
    elif option is "2":
        pass
    elif option is "3":
        pass
    elif option is "4":
        for path in PATHS:
            lineSeperator("=")
            print("Path: " + path)
            dirs = os.listdir(path)
            printProgressBar(0, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
            count = 1
            for i, d in enumerate(dirs):
                printProgressBar(i + 1, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
                if d is not ".DS_Store" and os.path.isdir(path + "/" + d):
                    innerD = os.listdir(path + "/" + d)
                    if ".DS_Store" in innerD:
                        innerD.remove(".DS_Store")
                    for dd in innerD:
                        if dd is not ".DS_Store" and os.path.isdir(path + "/" + d + "/" + dd):
                            createQrelsFile(path, d, dd)
                            count = createResFile(path, d, dd, count)
            lineSeperator("=")
    elif option is "5":
        pass
    elif option is "6":
        pass
    elif option is "7":
        pass
    else:
        print("Invalid Selection.")


if __name__ == "__main__":
    main()
