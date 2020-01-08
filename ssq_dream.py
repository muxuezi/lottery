# coding: utf-8

import numpy as np
import pandas as pd
from glob import glob
from nltk.util import ngrams

df = pd.read_csv("ssq.csv")

# 确定red_tag

# ![](http://img5.cache.netease.com/help/2013/2/5/20130205200221990eb.png)

bonus = {
    (0, 1): 5,
    (1, 1): 5,
    (2, 1): 5,
    (3, 1): 10,
    (4, 0): 10,
    (4, 1): 200,
    (5, 0): 200,
    (5, 1): 3000,
    (6, 0): 5000000,
    (6, 1): 10000000,
}
columns = ["red1", "red2", "red3", "red4", "red5", "red6", "blue"]
# 检查列表

topic, n = "ssq", 6

hot_water = sorted(glob(f"gamble/{topic}/*-{topic}.csv"))[-1]
date = hot_water[-18:-8]
df_dream = pd.read_csv(hot_water)

last_shit = df.loc[df.date <= date, "date"].max()
df_last = df.loc[df.date == last_shit, df_dream.columns]
list_last = df_last.values[0].tolist()
print(df.tail()[columns])


def getd(v):
    return len(set(v[:n]) & set(list_last[:n])), len(set(v[n:]) & set(list_last[n:]))


df_dream["check"] = df_dream.apply(getd, axis=1)
df_dream["bonus"] = df_dream.check.apply(lambda _: bonus.get(_, 0))
print(df_dream)
print("bonus", df_dream["bonus"].sum())

blue = df.blue.iloc[-1]
td = pd.datetime.today().date()
year = str(td.year)
yall = df.date.str.slice(0, 4)
ynum = yall.nunique() - 1
idx = yall == year

# other years blue average
key = pd.Series(ngrams(df.loc[~idx, "blue"], 2)).value_counts().to_frame("key")
dfkey = key.loc[[_ for _ in key.index if _[0] == blue]] / ynum
# this year blue
key2 = pd.Series(ngrams(df.loc[idx, "blue"], 2)).value_counts().to_frame("key2")
dfkey2 = key2.loc[[_ for _ in key2.index if _[0] == blue]]

dfkey = dfkey.join(dfkey2, how="left").fillna(0)
dfkey["key3"] = dfkey["key"] - dfkey["key2"]
dfkey.sort_values(by="key3", inplace=True)
blued = [b for _, b in dfkey.head().index]

# # 输出
idxa = (df.red1 <= 11) & (df.red6 >= 18)
t = len(df)
r = len(df[idxa]) / t * 100

# 剔除与最后一期交集>3

reds = df.loc[:, "red1":"red6"].apply(set, axis=1)
head = reds.iloc[:-1]
tail = reds.iloc[-1]


def get_pre(N):
    df_fore = (
        pd.concat(
            [
                reds.iloc[:i]
                .apply(lambda _: len(_ & reds.iloc[i]))
                .sort_index(ascending=False)
                .reset_index(drop=True)
                .to_frame(i)
                for i in reds.index[::-1][:N]
            ],
            axis=1,
        )
        .fillna(-1)
        .astype(int)
    )
    bar = df_fore.apply(lambda _: _.value_counts(), axis=1).fillna(-1).astype(int)
    return bar


bar = get_pre(4)
rst = []
for _ in range(5):
    p = len(reds) - np.random.choice(bar[bar[0] == 4].index, 2, replace=False) - 2
    red_drop = set()
    for i in reds.loc[p].values:
        red_drop |= i
    tmp = head[
        head.apply(
            lambda _: min(_)
            <= 11 & max(_)
            >= 18 & len(_ & red_drop)
            == 0 & len(_ & tail)
            <= 3
        )
    ]
    rst.append(df.loc[np.random.choice(tmp.index, 1,), "red1":"red6"])

ds = pd.concat(rst)

obj = set(np.reshape(ds.loc[:, "red1":"red6"].values, (1, 30))[0])
dr = sorted(set(range(1, 34)) - obj)
print(f"God bless! total {t} red1<=11 and red6>=18: {len(df[idxa])} {r:.1f}%")
print(f"ETL {len(bar)} unique {len(obj)} drop {dr}\n")

ds["blue"] = blued
ds.to_csv(f"gamble/ssq/{td}-ssq.csv", index=False)
print(ds)
