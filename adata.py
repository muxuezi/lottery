# %%
import pandas as pd
dlt = ['id','date','fore1','fore2','fore3','fore4','fore5','back1','back2','input_all','net_all','No1','No1_M','No2','No2_M','No3','No3_M','No4','No4_M','No5','No5_M','No6','No6_M','No7','No7_M','No8','No8_M', 'Append0', 'Append0_M', 'Append1', 'Append1_M', 'Append2', 'Append3', 'Append4', 'Append5', 'Append6']
ssq = ['id','date','red1','red2','red3','red4','red5','red6','blue','red1a','red2a','red3a','red4a','red5a','red6a','input_all','net_all','No1','No1_M','No2','No2_M','No3','No3_M','No4','No4_M','No5','No5_M','No6','No6_M']
# %%
df_ssq = pd.read_csv('https://www.17500.cn/getData/ssq.TXT', sep='\s+', names=ssq)
# %%
df_dlt = pd.read_csv('https://www.17500.cn/getData/dlt.TXT', sep='\s+', names=dlt, converters={'id':str})

#%%
df_ssq.to_csv('ssq.csv', index=False)
df_dlt.to_csv('dlt.csv', index=False)
td = pd.datetime.today().date()
print(td, 'Good Luck!')
