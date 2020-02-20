import trectools
import pandas as pd
import os

# %%

qrels_2017 = trectools.TrecQrel("data/clef_tar_complete/2017/testing/qrels/2017_test_abs.qrels")
qrels_2018 = trectools.TrecQrel("data/clef_tar_complete/2018/testing/qrels/2018_test_abs.qrels")
qrels_2019_d = trectools.TrecQrel("data/clef_tar_complete/2019/testing/DTA/qrels/2019_test_dta_abs.qrels")
qrels_2019_i = trectools.TrecQrel("data/clef_tar_complete/2019/testing/Intervention/qrels/2019_test_inter_abs.qrels")

# %%
years = ["2017/testing", "2018/testing", "2019/testing/DTA", "2019/testing/Intervention"]
results = ["original_full_query",
           "atm_result_query",
           "meta_result_query_all", "meta_result_query_one", "meta_result_query_topk",
           "umls_result_query_all", "umls_result_query_one", "umls_result_query_topk", ]

res_files = []
does_not_exist = []
for year in years:
    for result in results:
        runf = os.path.join("results", year, result) + ".res"
        yr = year.split("/")[0]
        if yr == "2019":
            if "DTA" in year:
                yr += "_d"
            else:
                yr += "_i"
        name = yr + "_" + result

        if os.path.isfile(runf):
            print(name)
            res_files.append((name, trectools.TrecRun(runf)))
        else:
            does_not_exist.append(name)

if len(does_not_exist) > 0:
    print("could not open the following files:")
    print(does_not_exist)

# %%

ev_files = []
for f in res_files:
    if f[0].startswith("2017"):
        q = qrels_2017
    elif f[0].startswith("2018"):
        q = qrels_2018
    elif f[0].startswith("2019_d"):
        q = qrels_2019_d
    elif f[0].startswith("2019_i"):
        q = qrels_2019_i
    else:
        raise Exception

    ev_files.append((f[0], trectools.TrecEval(f[1], q)))


# %%


def recall(e: trectools.TrecEval) -> float:
    return e.get_relevant_retrieved_documents(per_query=False) / e.get_relevant_documents(per_query=False)


def precision(e: trectools.TrecEval) -> float:
    return e.get_precision(depth=e.get_retrieved_documents(per_query=False), per_query=False)


def f_measure(e: trectools.TrecEval, beta: float = 1) -> float:
    p = precision(e)
    r = recall(e)
    return ((1 + beta) * (p * r)) / ((beta * p) + r)


def wss(e: trectools.TrecEval) -> float:
    ret = e.get_retrieved_documents()
    r = recall(e)
    N = 30000000
    wss = ((N - ret) / N) - (1.0 - r)
    if wss < 0: return 0
    return wss


def eval_set_df(e: trectools.TrecEval) -> pd.Series:
    return pd.Series({
        "P": precision(e),
        "F$_{0.5}$": f_measure(e, 0.5),
        "F$_1$": f_measure(e, 1),
        "F$_3$": f_measure(e, 3),
        "WSS": wss(e),
        "R": recall(e),
    })


# %%

df_ev = dict([(k, eval_set_df(v)) for k, v in ev_files])
# %%
df_results = pd.DataFrame(df_ev).T

# %%
print(df_results.to_latex(escape=False))
# %%
