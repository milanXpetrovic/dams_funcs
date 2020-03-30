# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 03:16:00 2020

@author: icecream_boi
"""


import os
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

def total_sleep(df):
    df = df.mean(axis=1)
    result = pd.DataFrame(df) #.reset_index(drop=True)
    result.columns = list(pop_name.split(" "))
    
    result.index = pd.to_datetime(result.index) 
    
    result = result.groupby([result.index.hour,
                             result.index.minute]).mean()
    
    return result
def draw_total_sleep(df, draw):
    
    for list_names in draw:
        result_table = pd.DataFrame()
        names = list_names.split(', ')
        dict_you_want = {your_key: experiments_df[your_key] for your_key in names}
        
        for pop_name, df in dict_you_want.items():  
            result = total_sleep(df)        
            result_table = pd.concat([result_table, result], axis=1)
            
        title = ','.join(names)
        result_table.to_csv('24_h_mean'+title+'.csv')
        result_table.plot.line()
        plt.title('24 sleeping activity for pop: ' + title)
        plt.legend(names)
        plt.show()
        #plt.clf()
        

## load files
path = r'F:\0_theory\biotech_data\sleep_analysis\sleep_fixed'
files = {}
for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.update({file[:-4] : os.path.join(r, file)})

#load experiments as df into dict
experiments_df = {}
for pop_name, path in files.items(): 
    print(pop_name)
    df = pd.read_csv(path, index_col=0, sep=',')
    df = df == 0 #ako gledamo aktivnost, ako zelimo spavanje onda == 0
    df = df*1
    df.index = pd.to_datetime(df.index) 
    experiments_df.update({pop_name : df})

draw = ['Elav-SOD3, Elav-SOD1, Elav-Gal4, CS-Ch',
        'DDC-SOD3, DDC-SOD2, DDC-Gal4, CS-Ch',
        'DDC-SOD3, Elav-SOD3, CS-Ch']

draw_total_sleep(experiments_df, draw)

def fun(df_day):
    res = df_day.between_time('20:00:00', '04:00:00')
    columns = list(res) 

    df_sleeping = {}
     
    for i in columns: 
        counter = 0
        for j in range(len(res[i])):
            counter +=1
            if res[i][j] == 1:
                df_sleeping.update({i: counter})
                break
    
    result_table = pd.DataFrame(list(df_sleeping.items()))
    result_table.index = result_table[0]
    result_table = result_table.drop([0], axis=1).T
    #print(result_table)
    
    return result_table


    
for pop_name, df in experiments_df.items():
    #print(pop_name, df.columns)
    
    resample = df.groupby(df.index.day).apply(fun).mean(axis=0)
    resample_sem = df.groupby(df.index.day).apply(fun).sem(axis=0)
    
    resample = pd.DataFrame(resample)
    x = np.array(resample.index)
    y = [x*5 for x in list(resample[0])]        
    e = np.array(resample_sem)
    
    plt.errorbar(x, y, e, linestyle='None', marker='o')
    
    plt.title('Time required for pop '+pop_name+' to fall asleep')
    plt.show()
    plt.clf()
