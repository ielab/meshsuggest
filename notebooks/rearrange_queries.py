import os
import shutil

if __name__ == '__main__':

    os.makedirs("queries/original_full_query/2017/testing", exist_ok=True)
    os.makedirs("queries/original_full_query/2018/testing", exist_ok=True)
    os.makedirs("queries/original_full_query/2019/testing/DTA/", exist_ok=True)
    os.makedirs("queries/original_full_query/2019/testing/Intervention", exist_ok=True)

    os.makedirs("queries/atm_result_query/2017/testing", exist_ok=True)
    os.makedirs("queries/atm_result_query/2018/testing", exist_ok=True)
    os.makedirs("queries/atm_result_query/2019/testing/DTA/", exist_ok=True)
    os.makedirs("queries/atm_result_query/2019/testing/Intervention", exist_ok=True)

    os.makedirs("queries/meta_result_query_all/2017/testing", exist_ok=True)
    os.makedirs("queries/meta_result_query_all/2018/testing", exist_ok=True)
    os.makedirs("queries/meta_result_query_all/2019/testing/DTA/", exist_ok=True)
    os.makedirs("queries/meta_result_query_all/2019/testing/Intervention", exist_ok=True)

    os.makedirs("queries/meta_result_query_one/2017/testing", exist_ok=True)
    os.makedirs("queries/meta_result_query_one/2018/testing", exist_ok=True)
    os.makedirs("queries/meta_result_query_one/2019/testing/DTA/", exist_ok=True)
    os.makedirs("queries/meta_result_query_one/2019/testing/Intervention", exist_ok=True)

    os.makedirs("queries/meta_result_query_topk/2017/testing", exist_ok=True)
    os.makedirs("queries/meta_result_query_topk/2018/testing", exist_ok=True)
    os.makedirs("queries/meta_result_query_topk/2019/testing/DTA/", exist_ok=True)
    os.makedirs("queries/meta_result_query_topk/2019/testing/Intervention", exist_ok=True)

    os.makedirs("queries/umls_result_query_all/2017/testing", exist_ok=True)
    os.makedirs("queries/umls_result_query_all/2018/testing", exist_ok=True)
    os.makedirs("queries/umls_result_query_all/2019/testing/DTA/", exist_ok=True)
    os.makedirs("queries/umls_result_query_all/2019/testing/Intervention", exist_ok=True)

    os.makedirs("queries/umls_result_query_one/2017/testing", exist_ok=True)
    os.makedirs("queries/umls_result_query_one/2018/testing", exist_ok=True)
    os.makedirs("queries/umls_result_query_one/2019/testing/DTA/", exist_ok=True)
    os.makedirs("queries/umls_result_query_one/2019/testing/Intervention", exist_ok=True)

    os.makedirs("queries/umls_result_query_topk/2017/testing", exist_ok=True)
    os.makedirs("queries/umls_result_query_topk/2018/testing", exist_ok=True)
    os.makedirs("queries/umls_result_query_topk/2019/testing/DTA/", exist_ok=True)
    os.makedirs("queries/umls_result_query_topk/2019/testing/Intervention", exist_ok=True)

    for year in ["2017/testing", "2018/testing", "2019/testing/DTA", "2019/testing/Intervention"]:
        for query in ["original_full_query", "atm_result_query",
                      "meta_result_query_all", "meta_result_query_one",  # TODO: topk, erm...
                      "umls_result_query_all", "umls_result_query_one"]:
            basedir = "data/clef_tar_processed/{}/".format(year)
            for file in os.listdir(basedir):
                if not os.path.isfile(os.path.join(basedir, file)):  # The path is a folder.
                    fdir = os.path.join(basedir, file, query)
                    shutil.copy(fdir, os.path.join("queries", query, year, file))
