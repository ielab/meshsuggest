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

    os.makedirs("queries/meta_result_query_100/2017/testing", exist_ok=True)
    os.makedirs("queries/meta_result_query_100/2018/testing", exist_ok=True)
    os.makedirs("queries/meta_result_query_100/2019/testing/DTA/", exist_ok=True)
    os.makedirs("queries/meta_result_query_100/2019/testing/Intervention", exist_ok=True)

    os.makedirs("queries/meta_result_query_topK/2017/testing", exist_ok=True)
    os.makedirs("queries/meta_result_query_topK/2018/testing", exist_ok=True)
    os.makedirs("queries/meta_result_query_topK/2019/testing/DTA/", exist_ok=True)
    os.makedirs("queries/meta_result_query_topK/2019/testing/Intervention", exist_ok=True)

    os.makedirs("queries/umls_result_query_100/2017/testing", exist_ok=True)
    os.makedirs("queries/umls_result_query_100/2018/testing", exist_ok=True)
    os.makedirs("queries/umls_result_query_100/2019/testing/DTA/", exist_ok=True)
    os.makedirs("queries/umls_result_query_100/2019/testing/Intervention", exist_ok=True)

    os.makedirs("queries/umls_result_query_topK/2017/testing", exist_ok=True)
    os.makedirs("queries/umls_result_query_topK/2018/testing", exist_ok=True)
    os.makedirs("queries/umls_result_query_topK/2019/testing/DTA/", exist_ok=True)
    os.makedirs("queries/umls_result_query_topK/2019/testing/Intervention", exist_ok=True)

    for year in ["2017/testing", "2018/testing", "2019/testing/DTA", "2019/testing/Intervention"]:
        for query in ["original_full_query", "atm_result_query",
                      "meta_result_query_100", "meta_result_query_topK",  # TODO: erm...
                      "umls_result_query_100", "umls_result_query_topK"]:
            basedir = "data/clef_tar_processed/{}/".format(year)
            for file in os.listdir(basedir):
                if not os.path.isfile(os.path.join(basedir, file)):  # The path is a folder.
                    fdir = os.path.join(basedir, file, query)
                    tdir = os.path.join("queries", query, year, file)
                    with open(fdir, "r") as f1:
                        q = f1.read()
                        q = q.replace(":noexp", "").replace("[mesh]", "[MeSH Terms]")
                        with open(tdir, "w") as f2:
                            f2.write(q)
