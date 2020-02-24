import subprocess

import trectools
import pandas as pd
import os

# %%

qrels_2017 = "data/clef_tar_complete/2017/testing/qrels/2017_test_abs.qrels"
qrels_2018 = "data/clef_tar_complete/2018/testing/qrels/2018_test_abs.qrels"
qrels_2019_d = "data/clef_tar_complete/2019/testing/DTA/qrels/2019_test_dta_abs.qrels"
qrels_2019_i = "data/clef_tar_complete/2019/testing/Intervention/qrels/2019_test_inter_abs.qrels"

# %%
years = ["2017/testing", "2018/testing", "2019/testing/DTA", "2019/testing/Intervention"]
results = ["original_full_query",
           "atm_result_query", "ltr_atm_result_query",
           "meta_result_query_100", "ltr_meta_result_query",
           "umls_result_query_100", "ltr_umls_result_query"]

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
            res_files.append((name, runf))
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

    ev_files.append((f[0], f[1], q))

# %%

# def rel_docs(e: trectools.TrecEval, per_query=False):
#     rel = e.get_relevant_documents(per_query=per_query)
#     ret = e.get_retrieved_documents(per_query=per_query)
#
#
# def recall(e: trectools.TrecEval, per_query=False):
#     rel_ret = e.get_relevant_retrieved_documents(per_query=per_query)
#     rel = e.get_relevant_documents(per_query=per_query)
#     print(rel_ret, rel)
#     if per_query:
#         return (rel_ret / rel).fillna(0)
#     else:
#         return rel_ret / rel
#
#
# def precision(e: trectools.TrecEval, per_query=False):
#     rel_ret = e.get_relevant_retrieved_documents(per_query=per_query)
#     ret = e.get_retrieved_documents(per_query=per_query)
#     if per_query:
#         return (rel_ret / ret).fillna(0)
#     else:
#         return rel_ret / ret
#
#
# def f_measure(e: trectools.TrecEval, beta: float = 1, per_query=False):
#     p = precision(e, per_query=per_query)
#     r = recall(e, per_query=per_query)
#     if per_query:
#         # return [((1 + beta) * (p.T[t] * r.T[t])) / ((beta * p.T[t]) + r.T[t]) for t in p.index]
#         return pd.Series(dict([(t, ((1 + beta) * (p.T[t] * r.T[t])) / ((beta * p.T[t]) + r.T[t])) for t in p.index])).fillna(0)
#     else:
#         return ((1 + beta) * (p * r)) / ((beta * p) + r)
#
#
# def wss(e: trectools.TrecEval, per_query=False):
#     ret = e.get_retrieved_documents(per_query=per_query)
#     r = recall(e, per_query=per_query)
#     N = 30000000
#     if per_query:
#         return pd.Series(dict([(t, (((N - ret.T[t]) / N) - (1.0 - r.T[t]))) for t in ret.index]))
#     else:
#         wss = ((N - ret) / N) - (1.0 - r)
#         if wss < 0: return 0  # don't ask.
#         return wss


# def eval_set_df(e: trectools.TrecEval, per_query=False) -> pd.Series:
#     return pd.Series({
#         "P": precision(e, per_query=per_query),
#         "F$_{0.5}$": f_measure(e, 0.5, per_query=per_query),
#         "F$_1$": f_measure(e, 1, per_query=per_query),
#         "F$_3$": f_measure(e, 3, per_query=per_query),
#         "WSS": wss(e, per_query=per_query),
#         "R": recall(e, per_query=per_query),
#     })


# %%

# metrics = ['MAP', 'RR', 'p@1', 'p@5', 'p@10', 'recall@1', 'recall@5', 'recall@10', 'NDCG']

ALL_ARGS = ['trec_eval', '-q', '-m', 'set_P', '-m', 'set_recall', '-m', 'set_F.0.5']
ALL_F1 = ['trec_eval', '-q', '-m', 'set_F.1']
ALL_F3 = ['trec_eval', '-q', '-m', 'set_F.3']


def to_trec_df(qrel_path: str, res_path: str, args=None, per_query=False):
    args = copy.copy(args)
    args += [qrel_path, res_path]
    args[0] = "trec_eval"
    print(args)
    res = subprocess.check_output(args)
    results = {}
    for line in res.decode('utf-8').split('\n'):
        parts = line.split()
        if len(parts) == 3:
            if parts[1] != "all":
                qry = parts[1]
                if qry not in results:
                    results[qry] = {}
                results[qry][parts[0]] = float(parts[2])
    df = pd.DataFrame.from_dict(results, orient='index')
    if not per_query:
        return df.mean(axis=0)
    return df


def trec_eval(qrel_path: str, res_path: str, per_query=False):
    if not per_query:
        df = to_trec_df(qrel_path, res_path, ALL_ARGS, per_query=per_query)
        df = df.append(to_trec_df(qrel_path, res_path, ALL_F1, per_query=per_query))
        df = df.append(to_trec_df(qrel_path, res_path, ALL_F3, per_query=per_query))
        return df
    df = to_trec_df(qrel_path, res_path, ALL_ARGS, per_query=per_query)
    df = df.join(to_trec_df(qrel_path, res_path, ALL_F1, per_query=per_query))
    df = df.join(to_trec_df(qrel_path, res_path, ALL_F3, per_query=per_query))
    return df


# %%

# df_ev = dict([(k, eval_set_df(v)) for k, v in ev_files])
# df_ev = dict([(a, to_trec_df(b, c, args=args, per_query=False)) for a, b, c in ev_files])
df_ev = dict([(a, trec_eval(c, b)) for a, b, c in ev_files])

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
df_eval = dict([(a, trec_eval(c, b, per_query=True)) for a, b, c in ev_files])
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
