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


def main():
    paths = [TOTAL_FOLDER_2017, TOTAL_FOLDER_2018, TOTAL_FOLDER_2019]
    for path in paths:
        print(path)
        dirs = os.listdir(path)
        for d in dirs:
            if d is not ".DS_Store" and os.path.isdir(path + "/" + d):
                innerD = os.listdir(path + "/" + d)
                if ".DS_Store" in innerD:
                    innerD.remove(".DS_Store")
                for dd in innerD:
                    print(d)
                    print(dd)
                    # mesh_f = open(path + "/" + d + "/" + dd + "/" + "mesh", "r")
                    # print(path + "/" + d + "/" + dd + "/" + "mesh")
                    # readFile(mesh_f)
                    clause_no_mesh_f = open(path + "/" + d + "/" + dd + "/" + "clean_clause", "r")
                    print(path + "/" + d + "/" + dd + "/" + "clean_clause")
                    readFile(clause_no_mesh_f)


if __name__ == "__main__":
    main()
