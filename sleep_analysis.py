# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:19:07 2019

@author: icecream boi
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:08:51 2019

@author: icecream boi
"""
import pandas as pd 
import matplotlib.pyplot as plt

#ucitavanje podataka
df = pd.read_csv(r'H:\1_Projects\biotech\DAM 1 bin\CTRL -2.txt', sep='\t', header=None, index_col=0)
df['datetime'] = df.iloc[:, 0] + ' ' + df.iloc[:, 1]
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.set_index(df['datetime'])
df.drop(df.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 29]], axis = 1, inplace = True) 
df = df.drop(columns=['datetime'])

df_mean = df.resample('H').mean().mean(axis=1)
#kreirati dataframe samo sa vrijednostima za C1, C2, C3, C4
#df = df[df.name.str.contains('^C')]
#visak columna, brisanje
#df = df.drop(['Unnamed: 0', 'monitor_status'], axis=1)
#df = df.groupby(['datetime']).mean()
#df = df.resample('H').mean()
#df.drop(df.columns[[15, 17, 18, 19, 20, 21, 22, 26, 30]], axis = 1, inplace = True) 
#columns = list(range(1, 24))
#df.columns = columns
#df.boxplot()
#df_day = df['2019-07-16 13:00:00':'2019-07-16 20:00:00']
#df_day.boxplot()

df_list =[]

for column in df:
    col =  df[column]
    column_sleeping = []
    for x in range(len(col)):
        window = x+5
        if window < len(col):
            selected = col[x:window]
            if sum(selected) == 0:
                column_sleeping.append('1')
            else:
                column_sleeping.append('0')
    df_list.append(column_sleeping)
 
df_sleeping = pd.DataFrame(df_list).T 

index_df = df.index  
index_df = index_df.drop(index_df[0:5])

df_sleeping = df_sleeping.set_index(index_df)

df_sleeping = df_sleeping.astype(str).astype(int)
df_sleeping = df_sleeping.resample('H').sum().mean(axis=1)

df_sleeping = df_sleeping.apply(lambda x: x/60*100)
plt.ylim(0,100) 

# Add title and axis names
plt.title('Average amount of Drosophila sleep per hour')
plt.ylabel('percent(%)')
plt.xlabel('time')

plt.plot(df_sleeping, 'k-^')
plt.gcf().autofmt_xdate()
plt.grid()
plt.savefig('sleep.png')

plt.show()

plt.title('Average amount of Drosophila activity per hour')
plt.ylabel('mean')
plt.xlabel('time')

plt.plot(df_mean, 'r-o') 
plt.gcf().autofmt_xdate()
plt.grid()
plt.savefig('activity.png')
plt.show()



