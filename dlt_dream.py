# coding: utf-8

import numpy as np
import pandas as pd
from glob import glob
df = pd.read_csv('dlt.csv')


# ![](http://img4.cache.netease.com/sports/2014/5/5/20140505211309dffc6.png)


bonus = {
    (0, 2): 5,
    (2, 1): 5,
    (1, 2): 5,
    (3, 0): 5,
    (2, 2): 10,
    (3, 1): 10,
    (4, 0): 10,
    (3, 2): 200,
    (4, 1): 200,
    (4, 2): 10,
    (5, 0): 10,
    (5, 1): 5000000,
    (5, 2): 10000000,
}


# 检查列表

topic, n = 'dlt', 5
hot_water = sorted(glob(f'gamble/{topic}/*-{topic}.csv'))[-1]
date = hot_water[-18:-8]
df_dream = pd.read_csv(hot_water)

last_shit = df.loc[df.date <= date, 'date'].max()
df_last = df.loc[df.date == last_shit, df_dream.columns]
list_last = df_last.values[0].tolist()
print(last_shit, list_last)


def getd(v):
    return len(set(v[:n]) & set(list_last[:n])), len(set(v[n:]) & set(list_last[n:]))


df_dream['check'] = df_dream.apply(getd, axis=1)
df_dream['bonus'] = df_dream.check.apply(lambda _: bonus.get(_, 0))
print(df_dream)
print('bonus', df_dream['bonus'].sum())

# 抽取新索引
td = str(pd.datetime.today().date())
np.random.seed()
bset = df.loc[:, 'fore1':'back2'].apply(set, axis=1)

ia = np.random.choice(df.index)
idx = [ia]
obj = bset[ia]
for i in range(4):
    ib = np.random.choice(bset.apply(
        lambda _: len(_ & obj)).nsmallest(10).index)
    idx.append(ib)
    obj |= bset[ib]

ds = df.loc[idx, ['fore1', 'fore2', 'fore3','fore4', 'fore5', 'back1', 'back2']]
obj = set(np.reshape(ds.loc[:, 'fore1':'fore5'].values, (1, 25))[0])
print('red', len(obj), sorted(set(range(1, 36)) - obj))
ds.to_csv(f'gamble/dlt/{td}-dlt.csv', index=False)
print(ds)
