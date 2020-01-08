
# coding: utf-8


# %load 3d_dream.py
import pandas as pd
from glob import glob


df = pd.read_csv('http://www.17500.cn/getData/3d.TXT', sep='\s+').iloc[:, :5]

df = df.T.reset_index().T.reset_index(drop=True)

df.columns = ['id', 'date', 'd1', 'd2', 'd3']
df.date = pd.DatetimeIndex(df.date)
df['year'] = df.date.dt.year
df['month'] = df.date.dt.month
df['day'] = df.date.dt.day
df['weekday'] = df.date.dt.weekday + 1
df[['d1', 'd2', 'd3']] = df[['d1', 'd2', 'd3']].astype(int)
df.eval('dsum = d1*100 + d2*10 + d3', inplace=True)

df.to_csv('3ds.csv', index=False)


# # 检查列表

topic, n = '3ds', 3

hot_water = sorted(glob(f'gamble/{topic}/*-{topic}.csv'))[-1]
date = hot_water[-18:-8]
df_dream = pd.read_csv(hot_water)

last_shit = df.loc[df.date <= date, 'date'].max()
df_last = df.loc[df.date == last_shit, df_dream.columns]
list_last = df_last.values[0].tolist()
print(last_shit.date(), list_last)


def getd(v):
    return len([(a, b) for a, b in zip(v, list_last) if a == b])


df_dream['check'] = df_dream.apply(getd, axis=1)
print(df_dream)


# # 计算下一期

def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val > 0 else 'black'
    return 'color: %s' % color


print(f'尚未出现：{set(range(1000)) - set(df.dsum.unique())}')


# dfg.style.applymap(color_negative_red)


# # 单球出现间隔


def get_blue(df_itv):
    df_itv_len = len(df_itv)
    tag_all = []
    h_interval = []
    blue_all = set(range(10))

    for idx, i in df_itv[::-1].iteritems():
        if i in blue_all:
            blue_all -= {i}
            # 当前间隔
            intv = df_itv_len - idx
            # 历史最大间隔
            unit = df_itv[df_itv == i].index
            foo = unit[1:] - unit[:-1]
            h_interval.append(pd.DataFrame(data=foo, columns=[i]))
            max_intv = max(foo)
            last_intv = foo[-1]
            tag_all.append((idx, i, intv, last_intv, max_intv,
                            intv - max_intv))
        if not blue_all:
            break

    df_back_s = pd.DataFrame(
        data=tag_all,
        columns=[
            'idx', 'ball', 'interval', 'last_interval', 'max_interval',
            'hope_intv'
        ])

    df_back_s.sort_values(by='hope_intv', ascending=False, inplace=True)
    # df_interval = pd.concat(h_interval, axis=1).sort_index(axis=1)
    return df_back_s.ball.values


# # 输出
td = pd.datetime.today().date()

ds = pd.DataFrame.from_dict(
    {_: get_blue(df[_])[:5]
     for _ in ['d1', 'd2', 'd3']})
ds.to_csv(f'gamble/3ds/{td}-3ds.csv', index=False)
print(ds)
