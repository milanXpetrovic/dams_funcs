"""
Created on Sat Oct 12 17:55:17 2019
@author: icecream boi
"""
import pandas as pd 

#ucitavanje podataka
df = pd.read_excel('results_2/16_17_7.xlsx')
df.drop(df.columns[[19, 21, 22, 23, 24, 25, 26, 30, 34]], axis = 1, inplace = True) 
#kreirati dataframe samo sa vrijednostima za C1, C2, C3, C4
df_C = df[df.name.str.contains('^C')]
df_ccc = df[df.name.str.contains('^C')]
#visak columna, brisanje
df_C = df_C.drop(['Unnamed: 0', 'monitor_status'], axis=1)
df_C = df_C.groupby(['datetime']).mean()
df_C = df_C.resample('H').sum().mean(axis=1)

df_D = df[df.name.str.contains('^D')] 
df_D = df_D.drop(['Unnamed: 0', 'monitor_status'], axis=1)
df_D = df_D.set_index('datetime')

df_D1 = df_D[df_D.name == 'D1'].drop(['name'], axis=1)
df_D1 = df_D1.resample('H').mean().mean(axis=1)

df_D2 = df_D[df_D.name == 'D2'].drop(['name'], axis=1)
df_D2 = df_D2.resample('H').mean().mean(axis=1)

df_D3 = df_D[df_D.name == 'D3'].drop(['name'], axis=1)
df_D3 = df_D3.resample('H').mean().mean(axis=1)

df_D4 = df_D[df_D.name == 'D4'].drop(['name'], axis=1)
df_D4 = df_D4.resample('H').mean().mean(axis=1)
#df_D = df_D.drop(['Unnamed: 0', 'monitor_status'], axis=1)

df_all = pd.concat([df_D1, df_D2, df_D3, df_D4], axis=1)
df_all.columns = ['D1', 'D2', 'D3', 'D4']

from datetime import datetime
import seaborn as sns; sns.set()
#df_all.index = pd.to_datetime(df_all.index)
ax = sns.heatmap(df_all, cmap="YlGnBu", vmin=0, vmax=100, annot=True)
ax.set_yticklabels(pd.to_datetime(df_all.index).strftime('%d-%m %H:%M'))

