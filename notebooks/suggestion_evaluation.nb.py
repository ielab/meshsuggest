import trectools
import pandas as pd

# %%

qrels_2017 = trectools.TrecQrel("data/clef_tar_processed/2017/testing/data.qrels")
qrels_2018 = trectools.TrecQrel("data/clef_tar_processed/2018/testing/data.qrels")
qrels_2019_d = trectools.TrecQrel("data/clef_tar_processed/2019/testing/DTA/data.qrels")
qrels_2019_i = trectools.TrecQrel("data/clef_tar_processed/2019/testing/Intervention/data.qrels")

# %%

res_atm_2017 = trectools.TrecRun("data/clef_tar_processed/2017/testing/atm.res")
res_atm_2018 = trectools.TrecRun("data/clef_tar_processed/2018/testing/atm.res")
res_atm_2019_d = trectools.TrecRun("data/clef_tar_processed/2019/testing/DTA/atm.res")
res_atm_2019_i = trectools.TrecRun("data/clef_tar_processed/2019/testing/Intervention/atm.res")

res_ltr_atm_2017 = trectools.TrecRun("ltr_res/test/cutoffs/2017_ATM_test_cutoff_5.res")
res_ltr_atm_2018 = trectools.TrecRun("ltr_res/test/cutoffs/2018_ATM_test_cutoff_5.res")
res_ltr_atm_2019_d = trectools.TrecRun("ltr_res/test/cutoffs/2019_ATM_D_test_cutoff_5.res")
res_ltr_atm_2019_i = trectools.TrecRun("ltr_res/test/cutoffs/2019_ATM_I_test_cutoff_5.res")

res_meta_all_2017 = trectools.TrecRun("data/clef_tar_processed/2017/testing/meta_100.res")
res_meta_all_2018 = trectools.TrecRun("data/clef_tar_processed/2018/testing/meta_100.res")
res_meta_all_2019_d = trectools.TrecRun("data/clef_tar_processed/2019/testing/DTA/meta_100.res")
res_meta_all_2019_i = trectools.TrecRun("data/clef_tar_processed/2019/testing/Intervention/meta_100.res")

res_ltr_meta_2017 = trectools.TrecRun("ltr_res/test/cutoffs/2017_Meta_test_cutoff_5.res")
res_ltr_meta_2018 = trectools.TrecRun("ltr_res/test/cutoffs/2018_Meta_test_cutoff_5.res")
res_ltr_meta_2019_d = trectools.TrecRun("ltr_res/test/cutoffs/2019_Meta_D_test_cutoff_5.res")
res_ltr_meta_2019_i = trectools.TrecRun("ltr_res/test/cutoffs/2019_Meta_I_test_cutoff_5.res")

# res_meta_top1_2017 = trectools.TrecRun("data/clef_tar_processed/2017/testing/meta_one.res")
# res_meta_top1_2018 = trectools.TrecRun("data/clef_tar_processed/2018/testing/meta_one.res")
# res_meta_top1_2019_d = trectools.TrecRun("data/clef_tar_processed/2019/testing/DTA/meta_one.res")
# res_meta_top1_2019_i = trectools.TrecRun("data/clef_tar_processed/2019/testing/Intervention/meta_one.res")
#
# res_meta_topk_2017 = trectools.TrecRun("data/clef_tar_processed/2017/testing/meta_topK.res")
# res_meta_topk_2018 = trectools.TrecRun("data/clef_tar_processed/2018/testing/meta_topK.res")
# res_meta_topk_2019_d = trectools.TrecRun("data/clef_tar_processed/2019/testing/DTA/meta_topK.res")
# res_meta_topk_2019_i = trectools.TrecRun("data/clef_tar_processed/2019/testing/Intervention/meta_topK.res")

res_umls_all_2017 = trectools.TrecRun("data/clef_tar_processed/2017/testing/umls_100.res")
res_umls_all_2018 = trectools.TrecRun("data/clef_tar_processed/2018/testing/umls_100.res")
res_umls_all_2019_d = trectools.TrecRun("data/clef_tar_processed/2019/testing/DTA/umls_100.res")
res_umls_all_2019_i = trectools.TrecRun("data/clef_tar_processed/2019/testing/Intervention/umls_100.res")

res_ltr_umls_2017 = trectools.TrecRun("ltr_res/test/cutoffs/2017_UMLS_test_cutoff_5.res")
res_ltr_umls_2018 = trectools.TrecRun("ltr_res/test/cutoffs/2018_UMLS_test_cutoff_5.res")
res_ltr_umls_2019_d = trectools.TrecRun("ltr_res/test/cutoffs/2019_UMLS_D_test_cutoff_5.res")
res_ltr_umls_2019_i = trectools.TrecRun("ltr_res/test/cutoffs/2019_UMLS_I_test_cutoff_5.res")

# res_umls_top1_2017 = trectools.TrecRun("data/clef_tar_processed/2017/testing/umls_one.res")
# res_umls_top1_2018 = trectools.TrecRun("data/clef_tar_processed/2018/testing/umls_one.res")
# res_umls_top1_2019_d = trectools.TrecRun("data/clef_tar_processed/2019/testing/DTA/umls_one.res")
# res_umls_top1_2019_i = trectools.TrecRun("data/clef_tar_processed/2019/testing/Intervention/umls_one.res")
#
# res_umls_topk_2017 = trectools.TrecRun("data/clef_tar_processed/2017/testing/umls_topK.res")
# res_umls_topk_2018 = trectools.TrecRun("data/clef_tar_processed/2018/testing/umls_topK.res")
# res_umls_topk_2019_d = trectools.TrecRun("data/clef_tar_processed/2019/testing/DTA/umls_topK.res")
# res_umls_topk_2019_i = trectools.TrecRun("data/clef_tar_processed/2019/testing/Intervention/umls_topK.res")

# %%

ev_2017_atm = trectools.TrecEval(res_atm_2017, qrels_2017)
ev_2018_atm = trectools.TrecEval(res_atm_2018, qrels_2018)
ev_2019_atm_d = trectools.TrecEval(res_atm_2019_d, qrels_2019_d)
ev_2019_atm_i = trectools.TrecEval(res_atm_2019_i, qrels_2019_i)

ev_2017_ltr_atm = trectools.TrecEval(res_ltr_atm_2017, qrels_2017)
ev_2018_ltr_atm = trectools.TrecEval(res_ltr_atm_2018, qrels_2018)
ev_2019_ltr_atm_d = trectools.TrecEval(res_ltr_atm_2019_d, qrels_2019_d)
ev_2019_ltr_atm_i = trectools.TrecEval(res_ltr_atm_2019_i, qrels_2019_i)

ev_2017_meta_all = trectools.TrecEval(res_meta_all_2017, qrels_2017)
ev_2018_meta_all = trectools.TrecEval(res_meta_all_2018, qrels_2018)
ev_2019_meta_all_d = trectools.TrecEval(res_meta_all_2019_d, qrels_2019_d)
ev_2019_meta_all_i = trectools.TrecEval(res_meta_all_2019_i, qrels_2019_i)

ev_2017_ltr_meta = trectools.TrecEval(res_ltr_meta_2017, qrels_2017)
ev_2018_ltr_meta = trectools.TrecEval(res_ltr_meta_2018, qrels_2018)
ev_2019_ltr_meta_d = trectools.TrecEval(res_ltr_meta_2019_d, qrels_2019_d)
ev_2019_ltr_meta_i = trectools.TrecEval(res_ltr_meta_2019_i, qrels_2019_i)

# ev_2017_meta_top1 = trectools.TrecEval(res_meta_top1_2017, qrels_2017)
# ev_2018_meta_top1 = trectools.TrecEval(res_meta_top1_2018, qrels_2018)
# ev_2019_meta_top1_d = trectools.TrecEval(res_meta_top1_2019_d, qrels_2019_d)
# ev_2019_meta_top1_i = trectools.TrecEval(res_meta_top1_2019_i, qrels_2019_i)
#
# ev_2017_meta_topk = trectools.TrecEval(res_meta_topk_2017, qrels_2017)
# ev_2018_meta_topk = trectools.TrecEval(res_meta_topk_2018, qrels_2018)
# ev_2019_meta_topk_d = trectools.TrecEval(res_meta_topk_2019_d, qrels_2019_d)
# ev_2019_meta_topk_i = trectools.TrecEval(res_meta_topk_2019_i, qrels_2019_i)

ev_2017_umls_all = trectools.TrecEval(res_umls_all_2017, qrels_2017)
ev_2018_umls_all = trectools.TrecEval(res_umls_all_2018, qrels_2018)
ev_2019_umls_all_d = trectools.TrecEval(res_umls_all_2019_d, qrels_2019_d)
ev_2019_umls_all_i = trectools.TrecEval(res_umls_all_2019_i, qrels_2019_i)

ev_2017_ltr_umls = trectools.TrecEval(res_ltr_umls_2017, qrels_2017)
ev_2018_ltr_umls = trectools.TrecEval(res_ltr_umls_2018, qrels_2018)
ev_2019_ltr_umls_d = trectools.TrecEval(res_ltr_umls_2019_d, qrels_2019_d)
ev_2019_ltr_umls_i = trectools.TrecEval(res_ltr_umls_2019_i, qrels_2019_i)

# ev_2017_umls_top1 = trectools.TrecEval(res_umls_top1_2017, qrels_2017)
# ev_2018_umls_top1 = trectools.TrecEval(res_umls_top1_2018, qrels_2018)
# ev_2019_umls_top1_d = trectools.TrecEval(res_umls_top1_2019_d, qrels_2019_d)
# ev_2019_umls_top1_i = trectools.TrecEval(res_umls_top1_2019_i, qrels_2019_i)
#
# ev_2017_umls_topk = trectools.TrecEval(res_umls_topk_2017, qrels_2017)
# ev_2018_umls_topk = trectools.TrecEval(res_umls_topk_2018, qrels_2018)
# ev_2019_umls_topk_d = trectools.TrecEval(res_umls_topk_2019_d, qrels_2019_d)
# ev_2019_umls_topk_i = trectools.TrecEval(res_umls_topk_2019_i, qrels_2019_i)


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
    ret = e.get_retrieved_documents(per_query=True)
    r = recall(e, per_query=per_query)
    N = 30000000
    if per_query:
        return pd.Series(dict([(t, (((N - ret.T[t]) / N) - (1.0 - r.T[t]))) for t in ret.index]))
    else:
        wss = ((N - ret) / N) - (1.0 - r)
        if wss < 0: return 0  # don't ask.
        return wss


def eval_set_df(e: trectools.TrecEval, per_query=True) -> pd.Series:
    return join_series(pd.Series({
        "P": precision(e, per_query=per_query),
        "R": recall(e, per_query=per_query),
        # "F$_{0.5}$": f_measure(e, 0.5, per_query=per_query),
        # "F$_1$": f_measure(e, 1, per_query=per_query),
        "NumRet": e.get_retrieved_documents(per_query=per_query)
        # "F$_3$": f_measure(e, 3, per_query=per_query),
    }), eval_rank_df(e, per_query=per_query))


def eval_rank_df(e: trectools.TrecEval, per_query=True) -> pd.Series:
    return pd.Series({
        "nDCG@5": e.get_ndcg(depth=5, per_query=per_query),
        "nDCG@10": e.get_ndcg(depth=10, per_query=per_query),
        "nDCG@20": e.get_ndcg(depth=20, per_query=per_query),
        "RR": e.get_reciprocal_rank(per_query=per_query)
    })


# %%

def join_series(x, y):
    return pd.DataFrame(x).T.join(pd.DataFrame(y).T).T[0]


def df_ev(per_query=True):
    return {
        "2017 ATM": eval_set_df(ev_2017_atm, per_query=per_query),
        "2017 ATM LTR": eval_set_df(ev_2017_ltr_atm, per_query=per_query),
        # "2017 M top-k": eval_set_df(ev_2017_meta_topk, per_query=per_query),
        "2017 M all": eval_set_df(ev_2017_meta_all, per_query=per_query),
        "2017 M LTR": eval_set_df(ev_2018_ltr_meta, per_query=per_query),
        # "2017 MetaMap top-1": eval_set_df(ev_2017_meta_top1, per_query=per_query),
        # "2017 U top-k": eval_set_df(ev_2017_umls_topk, per_query=per_query),
        "2017 U all": eval_set_df(ev_2017_umls_all, per_query=per_query),
        "2017 U LTR": eval_set_df(ev_2017_ltr_umls, per_query=per_query),
        # "2017 UMLS top-1": eval_set_df(ev_2017_umls_top1, per_query=per_query),

        "2018 ATM": eval_set_df(ev_2018_atm, per_query=per_query),
        "2018 ATM LTR": eval_set_df(ev_2018_ltr_atm, per_query=per_query),
        # "2018 M top-k": eval_set_df(ev_2018_meta_topk, per_query=per_query),
        "2018 M all": eval_set_df(ev_2018_meta_all, per_query=per_query),
        "2018 M LTR": eval_set_df(ev_2018_ltr_meta, per_query=per_query),
        # "2018 U top-k": eval_set_df(ev_2018_umls_topk, per_query=per_query),
        "2018 U all": eval_set_df(ev_2018_umls_all, per_query=per_query),
        "2018 U LTR": eval_set_df(ev_2018_ltr_umls, per_query=per_query),
        # "2018 UMLS top-1": eval_set_df(ev_2018_umls_top1, per_query=per_query),

        "2019 D ATM": eval_set_df(ev_2019_atm_d, per_query=per_query),
        "2019 D ATM LTR": eval_set_df(ev_2019_ltr_atm_d, per_query=per_query),
        # "2019 D M top-k": eval_set_df(ev_2019_meta_topk_d, per_query=per_query),
        "2019 D M all": eval_set_df(ev_2019_meta_all_d, per_query=per_query),
        "2019 D M LTR": eval_set_df(ev_2019_ltr_meta_d, per_query=per_query),
        # "2019 D MetaMap top-1": eval_set_df(ev_2019_meta_top1_d, per_query=per_query),
        # "2019 D U top-k": eval_set_df(ev_2019_umls_topk_d, per_query=per_query),
        "2019 D U all": eval_set_df(ev_2019_umls_all_d, per_query=per_query),
        "2019 D U LTR": eval_set_df(ev_2019_ltr_umls_d, per_query=per_query),
        # "2019 D UMLS top-1": eval_set_df(ev_2019_umls_top1_d, per_query=per_query),

        "2019 I ATM": eval_set_df(ev_2019_atm_i, per_query=per_query),
        "2019 I ATM LTR": eval_set_df(ev_2019_ltr_atm_i, per_query=per_query),
        # "2019 I M tok-k": eval_set_df(ev_2019_meta_topk_i, per_query=per_query),
        "2019 I M all": eval_set_df(ev_2019_meta_all_i, per_query=per_query),
        "2019 I M LTR": eval_set_df(ev_2019_ltr_meta_i, per_query=per_query),
        # "2019 I MetaMap top-1": eval_set_df(ev_2019_meta_top1_i, per_query=per_query),
        # "2019 I U top-k": eval_set_df(ev_2019_umls_topk_i, per_query=per_query),
        "2019 I U all": eval_set_df(ev_2019_umls_all_i, per_query=per_query),
        "2019 I U LTR": eval_set_df(ev_2019_ltr_umls_i, per_query=per_query)
        # "2019 I UMLS top-1": eval_set_df(ev_2019_umls_top1_i, per_query=per_query),
    }


df_results = pd.DataFrame(df_ev(per_query=False)).T

# %%
import scipy.stats as stats

# print(df_results.to_latex(escape=False, float_format="%.4f", formatters=[bold_max]))
d = pd.DataFrame()
t = df_results.copy()
df_eval = df_ev(per_query=True)
df = t.T
df2 = t.T
strs = []
# %%
s = {}
for x in df:
    for i in df[x].index:
        p = 1000
        k = "2017 A"
        if x.startswith("2018"):
            k = "2018 A"
        elif x.startswith("2019 D"):
            k = "2019 D A"
        elif x.startswith("2019 I"):
            k = "2019 I A"
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
