from metamap_helper import *
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
    print("1. Run ATM Method")
    print("2. Run MetaMap Method And Generate Res File")
    print("3. Run UMLS Method And Generate Res File")
    print("4. Generate qrels and result file for ATM")
    print("5. Entity Retrieval")
    print("6. Clean All Generated Files")
    option = input("Selection: ")
    if option is "1":
        for path in TEST:
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
        for path in TEST:
            lineSeperator("=")
            writeFile(path, "meta_progress", ENDBLOCK)
            writeFile(path, "meta_result", ENDBLOCK)
            print("Dataset: " + path)
            writeFile(path, "meta_progress", path + "\n")
            writeFile(path, "meta_result", path + "\n")
            dirs = os.listdir(path)
            totalHits = 0
            totalMeSHs = 0
            totalGen = 0
            count = 0
            rank = 1
            printProgressBar(0, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
            for i, d in enumerate(dirs):
                printProgressBar(i + 1, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
                if d is not ".DS_Store" and os.path.isdir(path + "/" + d):
                    innerD = os.listdir(path + "/" + d)
                    if ".DS_Store" in innerD:
                        innerD.remove(".DS_Store")
                    count += len(innerD)
                    fullNewMetaQuery = ""
                    for dd in innerD:
                        if dd is not ".DS_Store" and os.path.isdir(path + "/" + d + "/" + dd):
                            writeFile(path, "meta_progress", LINEBREAK)
                            writeFile(path, "meta_progress", "Topic: " + d + "\n")
                            writeFile(path, "meta_progress", "Sub-Clause: " + dd + "\n")
                            writeFile(path, "meta_progress",
                                      "Original MeSH Path: " + path + "/" + d + "/" + dd + "/" + "mesh" + "\n")
                            writeFile(path, "meta_progress",
                                      "Keyword Path: " + path + "/" + d + "/" + dd + "/" + "keywords" + "\n")
                            keywordF = open(path + "/" + d + "/" + dd + "/" + "keywords")
                            meshF = open(path + "/" + d + "/" + dd + "/" + "mesh", "r")
                            generatedMeshs, cleanedOriMeshs = getMetaMeshTerms(path, keywordF, meshF)
                            rank = createMetaResFile(path, d, dd, generatedMeshs, rank)
                            newQuery = generateNewMetaQuery(path + "/" + d + "/" + dd, generatedMeshs)
                            if fullNewMetaQuery is "":
                                fullNewMetaQuery = newQuery
                            else:
                                fullNewMetaQuery = fullNewMetaQuery + " AND " + newQuery
                            hits = findMatch(cleanedOriMeshs, generatedMeshs)
                            totalMeSHs += len(cleanedOriMeshs)
                            totalGen += len(generatedMeshs)
                            totalHits += len(hits)
                            writeFile(path, "meta_progress",
                                      "Number of Original MeSH Terms: " + str(len(cleanedOriMeshs)) + "\n")
                            writeFile(path, "meta_progress",
                                      "Number of MetaMap Generated MeSH Terms: " + str(len(generatedMeshs)) + "\n")
                            writeFile(path, "meta_progress", "Number of Terms Matched: " + str(len(hits)) + "\n")
                            writeFile(path, "meta_progress",
                                      "Recall: " + str((round(len(hits) / len(cleanedOriMeshs), 4)) * 100) + "%" + "\n")
                            if len(generatedMeshs) is 0:
                                pre = 0
                            else:
                                pre = (round(len(hits) / len(generatedMeshs), 4)) * 100
                            writeFile(path, "meta_progress", "Precision: " + str(pre) + "%" + "\n")
                            writeFile(path, "meta_progress", LINEBREAK)
                    writeFile(path + "/" + d, "meta_result_query", fullNewMetaQuery)
            writeFile(path, "meta_progress", LINEBREAK)
            writeFile(path, "meta_result", LINEBREAK)
            print("Total Sub-Clauses: " + str(count))
            writeFile(path, "meta_progress", "Total Sub-Clauses: " + str(count) + "\n")
            writeFile(path, "meta_result", "Total Sub-Clauses: " + str(count) + "\n")
            print("Total Original MeSH Terms: " + str(totalMeSHs))
            writeFile(path, "meta_progress", "Total Original MeSH Terms: " + str(totalMeSHs) + "\n")
            writeFile(path, "meta_result", "Total Original MeSH Terms: " + str(totalMeSHs) + "\n")
            print("Total Generated MeSH Terms: " + str(totalGen))
            writeFile(path, "meta_progress", "Total Generated MeSH Terms: " + str(totalGen) + "\n")
            writeFile(path, "meta_result", "Total Generated MeSH Terms: " + str(totalGen) + "\n")
            print("Total Matched MeSH Terms: " + str(totalHits))
            writeFile(path, "meta_progress", "Total Matched MeSH Terms: " + str(totalHits) + "\n")
            writeFile(path, "meta_result", "Total Matched MeSH Terms: " + str(totalHits) + "\n")
            print("Overall Recall: " + str((round(totalHits / totalMeSHs, 4)) * 100) + "%")
            writeFile(path, "meta_progress",
                      "Overall Recall: " + str((round(totalHits / totalMeSHs, 4)) * 100) + "%" + "\n")
            writeFile(path, "meta_result",
                      "Overall Recall: " + str((round(totalHits / totalMeSHs, 4)) * 100) + "%" + "\n")
            if totalGen is 0:
                opre = 0
            else:
                opre = (round(totalHits / totalGen, 4)) * 100
            print("Overall Precision: " + str(opre) + "%")
            writeFile(path, "meta_progress",
                      "Overall Precision: " + str((round(totalHits / totalGen, 4)) * 100) + "%" + "\n")
            writeFile(path, "meta_result",
                      "Overall Precision: " + str((round(totalHits / totalGen, 4)) * 100) + "%" + "\n")
            writeFile(path, "meta_progress", ENDBLOCK)
            writeFile(path, "meta_result", ENDBLOCK)
            lineSeperator("=")
    elif option is "3":
        for path in TEST:
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
        for path in PATHS:
            dirs = os.listdir(path)
            if os.path.isfile(path + "/" + "data.qrels"):
                os.remove(path + "/" + "data.qrels")
            if os.path.isfile(path + "/" + "atm.res"):
                os.remove(path + "/" + "atm.res")
            if os.path.isfile(path + "/" + "atm_progress"):
                os.remove(path + "/" + "atm_progress")
            if os.path.isfile(path + "/" + "atm_result"):
                os.remove(path + "/" + "atm_result")
            if os.path.isfile(path + "/" + "meta.res"):
                os.remove(path + "/" + "meta.res")
            if os.path.isfile(path + "/" + "meta_progress"):
                os.remove(path + "/" + "meta_progress")
            if os.path.isfile(path + "/" + "meta_result"):
                os.remove(path + "/" + "meta_result")
            if os.path.isfile(path + "/" + "umls.res"):
                os.remove(path + "/" + "umls.res")
            if os.path.isfile(path + "/" + "umls_result"):
                os.remove(path + "/" + "umls_result")
            if os.path.isfile(path + "/" + "umls_progress"):
                os.remove(path + "/" + "umls_progress")
            for d in dirs:
                if os.path.isfile(path + "/" + d + "/" + "atm_result_query"):
                    os.remove(path + "/" + d + "/" + "atm_result_query")
                if os.path.isfile(path + "/" + d + "/" + "original_full_query"):
                    os.remove(path + "/" + d + "/" + "original_full_query")
                if os.path.isfile(path + "/" + d + "/" + "meta_result_query"):
                    os.remove(path + "/" + d + "/" + "meta_result_query")
                if os.path.isfile(path + "/" + d + "/" + "umls_result_query"):
                    os.remove(path + "/" + d + "/" + "umls_result_query")
        print("Done")
    else:
        print("Invalid Selection.")


if __name__ == "__main__":
    main()
