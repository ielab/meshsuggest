from umls_helper import *
from generator import *
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

PATHS = [TEST_FOLDER_2017, TRAIN_FOLDER_2017, TOTAL_FOLDER_2017,
         TEST_FOLDER_2018, TRAIN_FOLDER_2018, TOTAL_FOLDER_2018,
         TEST_DTA_FOLDER_2019, TEST_INTERVENTION_FOLDER_2019, TOTAL_TEST_FOLDER_2019,
         TRAIN_DTA_FOLDER_2019, TRAIN_INTERVENTION_FOLDER_2019, TOTAL_TRAIN_FOLDER_2019,
         TOTAL_FOLDER_2019, TOTAL_DATASET]

TRAIN_SETS = [TRAIN_FOLDER_2017, TRAIN_FOLDER_2018, TRAIN_DTA_FOLDER_2019, TRAIN_INTERVENTION_FOLDER_2019,
              TOTAL_TRAIN_FOLDER_2019]

TEST_SETS = [TEST_FOLDER_2017, TEST_FOLDER_2018, TEST_DTA_FOLDER_2019, TEST_INTERVENTION_FOLDER_2019,
             TOTAL_TEST_FOLDER_2019]

RESPONSE_GENERATOR = [TOTAL_DATASET]

TEST = ["test"]


def main():
    print("1. Run With 6 Topics")
    print("2. Run All Datasets")
    print("3. Run On Train Sets")
    print("4. Run On Test Sets")
    print("5. Run On Response Generator")
    dataset = input("Selection: ")
    print("-----------------------------------------------------")
    print("1. Run ATM Method And Generate Res Files")
    print("2. Run MetaMap Method And Generate Res Files")
    print("3. Run UMLS Method And Generate Res Files")
    print("4. Run Entity Retrieval Method And Generate Res Files")
    print("5. Get MetaMap And UMLS Responses File")
    print("6. Generate Qrels Files")
    print("7. Clean All Generated Files (Be Careful to Use This)")
    option = input("Selection: ")
    if dataset is "2":
        selectedPath = PATHS
    elif dataset is "3":
        selectedPath = TRAIN_SETS
    elif dataset is "4":
        selectedPath = TEST_SETS
    else:
        selectedPath = TEST
    if option is "1":
        for path in selectedPath:
            lineSeperator("=")
            writeFile(path, "atm_progress", ENDBLOCK)
            writeFile(path, "atm_result", ENDBLOCK)
            print("Dataset: " + path)
            writeFile(path, "atm_progress", path + "\n")
            writeFile(path, "atm_result", path + "\n")
            dirs = os.listdir(path)
            totalMeSHs = 0
            totalGen = 0
            count = 0
            printProgressBar(0, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
            for i, d in enumerate(dirs):
                printProgressBar(i + 1, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
                if os.path.isdir(path + "/" + d):
                    innerD = os.listdir(path + "/" + d)
                    for x in innerD:
                        if not os.path.isdir(path + "/" + d + "/" + x):
                            innerD.remove(x)
                    count += len(innerD)
                    fullNewATMQuery = ""
                    fullOriginalQuery = ""
                    for dd in innerD:
                        if os.path.isdir(path + "/" + d + "/" + dd):
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
                            createResFile(path, d, dd, generatedMesh)
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
                            totalMeSHs += len(originalMesh)
                            totalGen += len(generatedMesh)
                            writeFile(path, "atm_progress", LINEBREAK)
                            writeFile(path, "atm_progress",
                                      "Number of Original MeSH Terms: " + str(len(originalMesh)) + "\n")
                            writeFile(path, "atm_progress",
                                      "Number of ATM Generated MeSH Terms: " + str(len(generatedMesh)) + "\n")
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
            writeFile(path, "atm_progress", ENDBLOCK)
            writeFile(path, "atm_result", ENDBLOCK)
            lineSeperator("=")
    elif option is "2":
        print("-----------------------------------------------------")
        print("Percentage (10 Means 10%): ")
        print("(all: Use All; one: Use Top 1)")
        num = input("Input: ")
        for path in selectedPath:
            lineSeperator("=")
            writeFile(path, "meta_progress_" + num, ENDBLOCK)
            writeFile(path, "meta_result_" + num, ENDBLOCK)
            print("Dataset: " + path)
            writeFile(path, "meta_progress_" + num, path + "\n")
            writeFile(path, "meta_result_" + num, path + "\n")
            dirs = os.listdir(path)
            totalMeSHs = 0
            totalGen = 0
            count = 0
            printProgressBar(0, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
            for i, d in enumerate(dirs):
                printProgressBar(i + 1, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
                if os.path.isdir(path + "/" + d):
                    innerD = os.listdir(path + "/" + d)
                    for x in innerD:
                        if not os.path.isdir(path + "/" + d + "/" + x):
                            innerD.remove(x)
                    count += len(innerD)
                    fullNewMetaQuery = ""
                    for dd in innerD:
                        if os.path.isdir(path + "/" + d + "/" + dd):
                            writeFile(path, "meta_progress_" + num, LINEBREAK)
                            writeFile(path, "meta_progress_" + num, "Topic: " + d + "\n")
                            writeFile(path, "meta_progress_" + num, "Sub-Clause: " + dd + "\n")
                            writeFile(path, "meta_progress_" + num,
                                      "Original MeSH Path: " + path + "/" + d + "/" + dd + "/" + "mesh" + "\n")
                            writeFile(path, "meta_progress_" + num,
                                      "Keyword Path: " + path + "/" + d + "/" + dd + "/" + "keywords" + "\n")
                            keywordF = open(path + "/" + d + "/" + dd + "/" + "keywords", "r")
                            meshF = open(path + "/" + d + "/" + dd + "/" + "mesh", "r")
                            generatedMeshs, cleanedOriMeshs = getMetaMeshTerms(path, keywordF, meshF, num)
                            createMetaResFile(path, d, dd, generatedMeshs, num)
                            newQuery = generateNewMetaQuery(path + "/" + d + "/" + dd, generatedMeshs)
                            if fullNewMetaQuery is "":
                                fullNewMetaQuery = newQuery
                            else:
                                fullNewMetaQuery = fullNewMetaQuery + " AND " + newQuery
                            totalMeSHs += len(cleanedOriMeshs)
                            totalGen += len(generatedMeshs)
                            writeFile(path, "meta_progress_" + num,
                                      "Number of Original MeSH Terms: " + str(len(cleanedOriMeshs)) + "\n")
                            writeFile(path, "meta_progress_" + num,
                                      "Number of MetaMap Generated MeSH Terms: " + str(len(generatedMeshs)) + "\n")
                            writeFile(path, "meta_progress_" + num, LINEBREAK)
                    writeFile(path + "/" + d, "meta_result_query_" + num, fullNewMetaQuery)
            writeFile(path, "meta_progress_" + num, LINEBREAK)
            writeFile(path, "meta_result_" + num, LINEBREAK)
            print("Total Sub-Clauses: " + str(count))
            writeFile(path, "meta_progress_" + num, "Total Sub-Clauses: " + str(count) + "\n")
            writeFile(path, "meta_result_" + num, "Total Sub-Clauses: " + str(count) + "\n")
            print("Total Original MeSH Terms: " + str(totalMeSHs))
            writeFile(path, "meta_progress_" + num, "Total Original MeSH Terms: " + str(totalMeSHs) + "\n")
            writeFile(path, "meta_result_" + num, "Total Original MeSH Terms: " + str(totalMeSHs) + "\n")
            print("Total Generated MeSH Terms: " + str(totalGen))
            writeFile(path, "meta_progress_" + num, "Total Generated MeSH Terms: " + str(totalGen) + "\n")
            writeFile(path, "meta_result_" + num, "Total Generated MeSH Terms: " + str(totalGen) + "\n")
            writeFile(path, "meta_progress_" + num, ENDBLOCK)
            writeFile(path, "meta_result_" + num, ENDBLOCK)
            lineSeperator("=")
    elif option is "3":
        print("-----------------------------------------------------")
        print("Percentage (10 Means 10%): ")
        print("(all: Use All; one: Use Top 1)")
        num = input("Input: ")
        for path in selectedPath:
            lineSeperator("=")
            writeFile(path, "umls_progress_" + num, ENDBLOCK)
            writeFile(path, "umls_result_" + num, ENDBLOCK)
            print("Dataset: " + path)
            writeFile(path, "umls_progress_" + num, path + "\n")
            writeFile(path, "umls_result_" + num, path + "\n")
            dirs = os.listdir(path)
            totalMeSHs = 0
            totalGen = 0
            count = 0
            printProgressBar(0, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
            for i, d in enumerate(dirs):
                printProgressBar(i + 1, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
                if os.path.isdir(path + "/" + d):
                    innerD = os.listdir(path + "/" + d)
                    for x in innerD:
                        if not os.path.isdir(path + "/" + d + "/" + x):
                            innerD.remove(x)
                    count += len(innerD)
                    fullNewUMLSQuery = ""
                    for dd in innerD:
                        if os.path.isdir(path + "/" + d + "/" + dd):
                            writeFile(path, "umls_progress_" + num, LINEBREAK)
                            writeFile(path, "umls_progress_" + num, "Topic: " + d + "\n")
                            writeFile(path, "umls_progress_" + num, "Sub-Clause: " + dd + "\n")
                            writeFile(path, "umls_progress_" + num,
                                      "Original MeSH Path: " + path + "/" + d + "/" + dd + "/" + "mesh" + "\n")
                            writeFile(path, "umls_progress_" + num,
                                      "Keyword Path: " + path + "/" + d + "/" + dd + "/" + "keywords" + "\n")
                            keywordF = open(path + "/" + d + "/" + dd + "/" + "keywords", "r")
                            meshF = open(path + "/" + d + "/" + dd + "/" + "mesh", "r")
                            generatedMeshs, cleanedOriMeshs = getUMLSMeshTerms(path, keywordF, meshF, num)
                            createUMLSResFile(path, d, dd, generatedMeshs, num)
                            newQuery = generateNewUMLSQuery(path + "/" + d + "/" + dd, generatedMeshs)
                            if fullNewUMLSQuery is "":
                                fullNewUMLSQuery = newQuery
                            else:
                                fullNewUMLSQuery = fullNewUMLSQuery + " AND " + newQuery
                            totalMeSHs += len(cleanedOriMeshs)
                            totalGen += len(generatedMeshs)
                            writeFile(path, "umls_progress_" + num,
                                      "Number of Original MeSH Terms: " + str(len(cleanedOriMeshs)) + "\n")
                            writeFile(path, "umls_progress_" + num,
                                      "Number of UMLS Generated MeSH Terms: " + str(len(generatedMeshs)) + "\n")
                            writeFile(path, "umls_progress_" + num, LINEBREAK)
                    writeFile(path + "/" + d, "umls_result_query_" + num, fullNewUMLSQuery)
            writeFile(path, "umls_progress_" + num, LINEBREAK)
            writeFile(path, "umls_result_" + num, LINEBREAK)
            print("Total Sub-Clauses: " + str(count))
            writeFile(path, "umls_progress_" + num, "Total Sub-Clauses: " + str(count) + "\n")
            writeFile(path, "umls_result_" + num, "Total Sub-Clauses: " + str(count) + "\n")
            print("Total Original MeSH Terms: " + str(totalMeSHs))
            writeFile(path, "umls_progress_" + num, "Total Original MeSH Terms: " + str(totalMeSHs) + "\n")
            writeFile(path, "umls_result_" + num, "Total Original MeSH Terms: " + str(totalMeSHs) + "\n")
            print("Total Generated MeSH Terms: " + str(totalGen))
            writeFile(path, "umls_progress_" + num, "Total Generated MeSH Terms: " + str(totalGen) + "\n")
            writeFile(path, "umls_result_" + num, "Total Generated MeSH Terms: " + str(totalGen) + "\n")
            writeFile(path, "umls_progress_" + num, ENDBLOCK)
            writeFile(path, "umls_result_" + num, ENDBLOCK)
            lineSeperator("=")
    elif option is "4":
        print("Method Not Implemented Yet!")
    elif option is "5":
        for path in selectedPath:
            dirs = os.listdir(path)
            for d in dirs:
                if os.path.isdir(path + "/" + d):
                    innerD = os.listdir(path + "/" + d)
                    for x in innerD:
                        if not os.path.isdir(path + "/" + d + "/" + x):
                            innerD.remove(x)
                    for dd in innerD:
                        if os.path.isdir(path + "/" + d + "/" + dd):
                            print("-----------------------------------------------------")
                            print(d + "/" + dd)
                            keywordF = open(path + "/" + d + "/" + dd + "/" + "keywords", "r")
                            writeUMLSAndMetaResponse(keywordF)
    elif option is "6":
        for path in selectedPath:
            lineSeperator("=")
            print("Path: " + path)
            dirs = os.listdir(path)
            printProgressBar(0, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
            for i, d in enumerate(dirs):
                printProgressBar(i + 1, len(dirs), prefix='Progress', suffix='Complete', autosize=True)
                if os.path.isdir(path + "/" + d):
                    innerD = os.listdir(path + "/" + d)
                    for x in innerD:
                        if not os.path.isdir(path + "/" + d + "/" + x):
                            innerD.remove(x)
                    for dd in innerD:
                        if os.path.isdir(path + "/" + d + "/" + dd):
                            createQrelsFile(path, d, dd)
            lineSeperator("=")
    elif option is "7":
        print("-----------------------------------------------------")
        print("Percentage (10 Means 10%) In UMLS: ")
        print("(all: Used All; one: Top 1)")
        num = input("Input: ")
        print("-----------------------------------------------------")
        print("Percentage (10 Means 10%) In MetaMap : ")
        print("(all: Used All; one: Top 1)")
        metaNum = input("Input: ")
        meta = os.listdir("metamap_responses")
        umls = os.listdir("umls_responses")
        for each in meta:
            os.remove("metamap_responses/" + each)
        for u in umls:
            os.remove("umls_responses/" + u)
        for path in selectedPath:
            dirs = os.listdir(path)
            if os.path.isfile(path + "/" + "data.qrels"):
                os.remove(path + "/" + "data.qrels")
            if os.path.isfile(path + "/" + "atm.res"):
                os.remove(path + "/" + "atm.res")
            if os.path.isfile(path + "/" + "atm_progress"):
                os.remove(path + "/" + "atm_progress")
            if os.path.isfile(path + "/" + "atm_result"):
                os.remove(path + "/" + "atm_result")
            if os.path.isfile(path + "/" + "meta_" + metaNum + ".res"):
                os.remove(path + "/" + "meta_" + metaNum + ".res")
            if os.path.isfile(path + "/" + "meta_progress_" + metaNum):
                os.remove(path + "/" + "meta_progress_" + metaNum)
            if os.path.isfile(path + "/" + "meta_result_" + metaNum):
                os.remove(path + "/" + "meta_result_" + metaNum)
            if os.path.isfile(path + "/" + "umls_" + num + ".res"):
                os.remove(path + "/" + "umls_" + num + ".res")
            if os.path.isfile(path + "/" + "umls_result_" + num):
                os.remove(path + "/" + "umls_result_" + num)
            if os.path.isfile(path + "/" + "umls_progress_" + num):
                os.remove(path + "/" + "umls_progress_" + num)
            for d in dirs:
                if os.path.isfile(path + "/" + d + "/" + "atm_result_query"):
                    os.remove(path + "/" + d + "/" + "atm_result_query")
                if os.path.isfile(path + "/" + d + "/" + "original_full_query"):
                    os.remove(path + "/" + d + "/" + "original_full_query")
                if os.path.isfile(path + "/" + d + "/" + "meta_result_query_" + metaNum):
                    os.remove(path + "/" + d + "/" + "meta_result_query_" + metaNum)
                if os.path.isfile(path + "/" + d + "/" + "umls_result_query_" + num):
                    os.remove(path + "/" + d + "/" + "umls_result_query_" + num)
        print("Done")
    else:
        print("Invalid Selection.")


if __name__ == "__main__":
    main()
