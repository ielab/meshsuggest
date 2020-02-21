import trectools
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.lines as mlines
import seaborn as sns
import scipy.stats as stats
import math
import json
import random
import os
import trectools
from trectools import fusion
from rbo import RankingSimilarity
from operator import itemgetter
import itertools
from sklearn.preprocessing import minmax_scale

from IPython.display import set_matplotlib_formats

set_matplotlib_formats('png')

# import libraries
import numpy as np
import collections

# Set general plot properties.
sns.set()
sns.set_context("paper")
sns.set_color_codes("pastel")

# This causes matplotlib to use Type 42 (a.k.a. TrueType) fonts for PostScript and PDF files.
# This allows you to avoid Type 3 fonts without limiting yourself to the stone-age technology
# of Type 1 fonts.
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

from matplotlib.colors import LogNorm
from matplotlib.mlab import bivariate_normal
from matplotlib.legend_handler import HandlerLine2D
import sys
import importlib

# %%

qrels_2017 = trectools.TrecQrel("data/clef_tar_processed/2017/training/data.qrels")
qrels_2018 = trectools.TrecQrel("data/clef_tar_processed/2018/training/data.qrels")
qrels_2019_d = trectools.TrecQrel("data/clef_tar_processed/2019/training/DTA/data.qrels")
qrels_2019_i = trectools.TrecQrel("data/clef_tar_processed/2019/training/Intervention/data.qrels")

# %%

incr = list(range(5, 100, 5))
meta_2017 = []
umls_2017 = []
meta_2018 = []
umls_2018 = []
meta_2019_d = []
umls_2019_d = []
meta_2019_i = []
umls_2019_i = []

for inc in incr:
    for year in ["2017/training", "2018/training", "2019/training/DTA", "2019/training/Intervention"]:
        if year == "2017/training":
            meta_2017.append(trectools.TrecRun("data/clef_tar_processed/{}/meta_{}.res".format(year, inc)))
            umls_2017.append(trectools.TrecRun("data/clef_tar_processed/{}/umls_{}.res".format(year, inc)))
        if year == "2018/training":
            meta_2018.append(trectools.TrecRun("data/clef_tar_processed/{}/meta_{}.res".format(year, inc)))
            umls_2018.append(trectools.TrecRun("data/clef_tar_processed/{}/umls_{}.res".format(year, inc)))
        if year == "2019/training/DTA":
            meta_2019_d.append(trectools.TrecRun("data/clef_tar_processed/{}/meta_{}.res".format(year, inc)))
            umls_2019_d.append(trectools.TrecRun("data/clef_tar_processed/{}/umls_{}.res".format(year, inc)))
        if year == "2019/training/Intervention":
            meta_2019_i.append(trectools.TrecRun("data/clef_tar_processed/{}/meta_{}.res".format(year, inc)))
            umls_2019_i.append(trectools.TrecRun("data/clef_tar_processed/{}/umls_{}.res".format(year, inc)))


# %%

def recall(e: trectools.TrecEval) -> float:
    return e.get_relevant_retrieved_documents(per_query=False) / e.get_relevant_documents(per_query=False)


def precision(e: trectools.TrecEval) -> float:
    return e.get_precision(depth=e.get_retrieved_documents(per_query=False), per_query=False)


def f_measure(e: trectools.TrecEval, beta: float = 1) -> float:
    p = precision(e)
    r = recall(e)
    if p == 0 and r == 0: return 0.0
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
        "R": recall(e),
        "F$_{0.5}$": f_measure(e, 0.5),
        "F$_1$": f_measure(e, 1),
        "F$_3$": f_measure(e, 3),
        "WSS": wss(e),
    })


def eval_rank_df(e: trectools.TrecEval) -> pd.Series:
    return pd.Series({
        "nDCG@5": e.get_ndcg(depth=5, per_query=False),
        "nDCG@10": e.get_ndcg(depth=10, per_query=False),
        "nDCG@20": e.get_ndcg(depth=20, per_query=False),
    })


# %%

def get_vals(runs, qrels):
    vals = []
    for i, run in enumerate(runs):
        ev = trectools.TrecEval(run, qrels)
        f1 = f_measure(ev, 1)
        vals.append((incr[i], f1))
    return vals


vals = [[[]] * 4, [[]] * 4, [[]] * 4]
vals[1][0] = get_vals(meta_2017, qrels_2017)
vals[1][1] = get_vals(meta_2018, qrels_2018)
vals[1][2] = get_vals(meta_2019_d, qrels_2019_d)
vals[1][3] = get_vals(meta_2019_i, qrels_2019_i)
vals[2][0] = get_vals(umls_2017, qrels_2017)
vals[2][1] = get_vals(umls_2018, qrels_2018)
vals[2][2] = get_vals(umls_2019_d, qrels_2019_d)
vals[2][3] = get_vals(umls_2019_i, qrels_2019_i)
# %%
titles = [[""] * 4, [""] * 4, [""] * 4]
titles[0][0] = "ERM 2017"
titles[0][1] = "ERM 2018"
titles[0][2] = "ERM 2019 (D)"
titles[0][3] = "ERM 2019 (I)"
titles[1][0] = "MetaMap 2017"
titles[1][1] = "MetaMap 2018"
titles[1][2] = "MetaMap 2019 (D)"
titles[1][3] = "MetaMap 2019 (I)"
titles[2][0] = "UMLS 2017"
titles[2][1] = "UMLS 2018"
titles[2][2] = "UMLS 2019 (D)"
titles[2][3] = "UMLS 2019 (I)"
# %%
plt.style.use('grayscale')
sns.set_style("whitegrid")
fig, axs = plt.subplots(3, 4)
for i in range(len(vals)):
    for j in range(len(vals[i])):
        ax = axs[i][j]
        lp = sns.lineplot(x=[x[0] for x in vals[i][j]], y=[x[1] for x in vals[i][j]], ax=ax).set(title=titles[i][j])
plt.tight_layout()
plt.savefig("plots/kappa.pdf")
plt.show()
# %%
for i in range(len(vals)):
    for j in range(len(vals[i])):
        s = pd.Series(dict(vals[i][j]))
        print(titles[i][j], ",", s.idxmax(), ",", s.max())
