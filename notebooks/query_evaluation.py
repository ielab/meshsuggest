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
           "meta_result_query_100",
           "umls_result_query_100", ]

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


def recall(e: trectools.TrecEval, per_query=False):
    rel_ret = e.get_relevant_retrieved_documents(per_query=per_query)
    rel = e.get_relevant_documents(per_query=per_query)
    if per_query:
        return (rel_ret / rel).fillna(0)
    else:
        return rel_ret / rel


def precision(e: trectools.TrecEval, per_query=False):
    rel_ret = e.get_relevant_retrieved_documents(per_query=per_query)
    rel = e.get_retrieved_documents(per_query=per_query)
    if per_query:
        return (rel_ret / rel).fillna(0)
    else:
        return rel_ret / rel


def f_measure(e: trectools.TrecEval, beta: float = 1, per_query=False):
    p = precision(e, per_query=per_query)
    r = recall(e, per_query=per_query)
    if per_query:
        # return [((1 + beta) * (p.T[t] * r.T[t])) / ((beta * p.T[t]) + r.T[t]) for t in p.index]
        return pd.Series(dict([(t, ((1 + beta) * (p.T[t] * r.T[t])) / ((beta * p.T[t]) + r.T[t])) for t in p.index])).fillna(0)
    else:
        return ((1 + beta) * (p * r)) / ((beta * p) + r)


def wss(e: trectools.TrecEval, per_query=False):
    ret = e.get_retrieved_documents(per_query=per_query)
    r = recall(e, per_query=per_query)
    N = 30000000
    if per_query:
        return pd.Series(dict([(t, (((N - ret.T[t]) / N) - (1.0 - r.T[t]))) for t in ret.index]))
    else:
        wss = ((N - ret) / N) - (1.0 - r)
        if wss < 0: return 0  # don't ask.
        return wss


def eval_set_df(e: trectools.TrecEval, per_query=False) -> pd.Series:
    return pd.Series({
        "P": precision(e, per_query=per_query),
        "F$_{0.5}$": f_measure(e, 0.5, per_query=per_query),
        "F$_1$": f_measure(e, 1, per_query=per_query),
        "F$_3$": f_measure(e, 3, per_query=per_query),
        "WSS": wss(e, per_query=per_query),
        "R": recall(e, per_query=per_query),
    })


# %%

df_ev = dict([(k, eval_set_df(v)) for k, v in ev_files])
# %%

df_results = pd.DataFrame(df_ev).T

# %%
print(df_results.to_latex(escape=False))
# %%
# %%
import scipy.stats as stats

# print(df_results.to_latex(escape=False, float_format="%.4f", formatters=[bold_max]))
d = pd.DataFrame()
t = df_results.copy()
df_eval = dict([(k, eval_set_df(v, per_query=True)) for k, v in ev_files])
df = t.T
df2 = t.T
strs = []
# %%
s = {}
for x in df:
    for i in df[x].index:
        p = 1000
        k = "2017_original_full_query"
        if x.startswith("2018"):
            k = "2018_original_full_query"
        elif x.startswith("2019"):
            k = "2019_d_original_full_query"
        elif x.startswith("2019"):
            k = "2019_i_original_full_query"
        if len(df_eval[k][i]) == len(df_eval[x][i]) and k != x:
            a = list(df_eval[k][i].values)
            b = list(df_eval[x][i].values)
            while len(a) < len(b):
                a.append(0)
            while len(b) < len(a):
                b.append(0)
            print(len(a), len(b))
            a = df_eval[k][i]
            b = df_eval[x][i]
            p = stats.ttest_rel(a, b).pvalue
        if x + i not in s:
            s[x + i] = []
        if p < 0.05:
            s[x + i].append('*')
for x in df:
    for i in df[x].index:
        if x + i in s:
            if df[x][i] <= 1:
                df2[x][i] = "{:.4f}".format(df[x][i]) + "$^{" + ",".join(s[x + i]) + "}$"
            else:
                df2[x][i] = "{}".format(int(df[x][i])) + "$^{" + ",".join(s[x + i]) + "}$"
print(df2.T.to_latex(escape=False))
# %%
