# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 03:16:00 2020

@author: icecream_boi
"""


import os
from itertools import groupby
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

def draw_total_sleep(df_experiments, draw):
    for list_names in draw:
        result_table = pd.DataFrame()
        names = list_names.split(', ')
        dict_you_want = {your_key: df_experiments[your_key] for your_key in names}
        
        for pop_name, df in dict_you_want.items():  
            result = total_sleep(df)        
            result_table = pd.concat([result_table, result], axis=1)
        
        result_table.columns = names   
        title = ','.join(names)
        result_table.to_csv('24_h_mean'+title+'.csv')
        result_table.plot.line()
        plt.title('24 sleeping activity for pop: ' + title)
        plt.legend(names)
        plt.show()
        
def sleep_after_eight(df_day):
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
    
    return result_table        

def draw_sleep_after_eight(df, pop_name):
    resample = df.groupby(df.index.day).apply(sleep_after_eight).mean(axis=0)
    resample_sem = df.groupby(df.index.day).apply(sleep_after_eight).sem(axis=0)
    
    resample = pd.DataFrame(resample)
    x = np.array(resample.index)
    y = [x*5 for x in list(resample[0])]        
    e = np.array(resample_sem)
    
    result_save = pd.concat([resample, resample_sem], axis=1)
    result_save.columns = ['mean', 'sem']
    result_save = result_save.T
    path = 'sleep_after_eight/' + pop_name + '.csv'
    result_save.to_csv(path)
    
    
    plt.errorbar(x, y, e, linestyle='None', marker='o')
    plt.axhline(y = sum(y)/len(y))
    plt.title('Time required for pop '+pop_name+' to fall asleep')
    #plt.show()
    path_png = 'sleep_after_eight/' + pop_name + '.png'
    plt.savefig(path_png)
    plt.clf()

## load files
path = r'F:\0_theory\biotech_data\sleep_analysis\sleep_fixed_analysis'
files = {}
for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.update({file[:-4] : os.path.join(r, file)})

#load experiments as df into dict
experiments_df = {}
for pop_name, path in files.items(): 
    df = pd.read_csv(path, index_col=0, sep=',')
    df = df == 0 #ako zelimo spavanje onda == 0
    df = df*1
    df.index = pd.to_datetime(df.index) 
    experiments_df.update({pop_name : df})

draw = ['Elav-SOD3, Elav-SOD1, Elav-Gal4, CS-Ch',
        'DDC-SOD3, DDC-SOD2, DDC-Gal4, CS-Ch',
        'DDC-SOD3, Elav-SOD3, CS-Ch']

#draw_total_sleep(experiments_df, draw)
def individual_interval_analysis(column):
    total_sleep = sum(column)
    total_activity = len(column) - total_sleep
    
    sleep_activity_intervals = [list(j) for i, j in groupby(column)]
    sleep_activity_intervals.sort(key=len, reverse=True)
    
    sleeping_intervals = [len(list) for list in sleep_activity_intervals if sum(list)>=1]
    activity_intervals = [len(list) for list in sleep_activity_intervals if sum(list)<1]
    
   
    try:
        longest_sleep_interval = max(sleeping_intervals)

    except ValueError:
        longest_sleep_interval = 0
        
    
    amount_sleep_intervals = len(sleeping_intervals)
    
    try:
        longest_activity_interval = max(activity_intervals) 

    except ValueError:
        longest_activity_interval = 0
        
    amount_activity_intervals = len(activity_intervals)
    
    return longest_sleep_interval, amount_sleep_intervals, longest_activity_interval, amount_activity_intervals, total_sleep, total_activity

def longest_sleep_interval(df, day_night, day_date_value):
    result_table_population = {}

    columns = list(df)
    index_day = day_night + ' '
    for column in columns:
        lsi, nsi, lai, nai, ts, ta= individual_interval_analysis(df[column])
        
        result_table_population.update({column:{index_day + 'longest_sleep_interval':lsi,
                                                index_day + 'numb_of_sleep_intervals':nsi,
                                                index_day + 'total_sleep': ts,
                                                index_day + 'longest_activity_interval':lai,
                                                index_day + 'numb_of_activity_interval':nai,
                                                index_day + 'total_activity': ta}})
        
    result_table_population = (pd.DataFrame(result_table_population))

    return result_table_population

def foo(df):
   
    day_date_value = int(df.head(1).index.day.values)
    
    if df.head(1).index.hour == 8:
        day_mean = longest_sleep_interval(df, 'day', day_date_value)
        return day_mean
        
    if df.head(1).index.hour == 20:
        night_mean = longest_sleep_interval(df, 'night', day_date_value)
        return night_mean

    
    
for pop_name, df in experiments_df.items():
    print(pop_name)
    #draw_sleep_after_eight(df, pop_name)
    resample = df.groupby(pd.Grouper(freq="12H", base=8, label='right')).apply(foo)
    
    resample.reset_index(inplace=True)
    resample[['day_period', 'measure']] = resample.level_1.str.split(expand=True)

    resample = resample.drop(['level_1'], axis=1)
    resample = resample.set_index(['level_0', 'day_period', 'measure'])
    
    mean_day_period_12h = resample.groupby(['day_period', 'measure']).mean()
    mean_measure_24h = resample.groupby('measure').mean()
    
    mean_day_period_12h.to_csv('sleep_measures/mean_day_period_12h.csv')
    mean_measure_24h.to_csv('sleep_measures/mean_measure_24h.csv')
