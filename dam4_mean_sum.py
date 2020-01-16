# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 21:45:52 2019

@author: icecream boi
"""
import pandas as pd 
import datetime
from dateutil import parser

def create_xlsx(df, start_time, end_time):
    
    start_time_name = parser.parse(start_time)
    start_time_name = start_time_name.strftime("%Y_%m_%d_%H_%M")

    end_time_name = parser.parse(end_time)
    end_time_name = end_time_name.strftime("%Y_%m_%d_%H_%M")
    
    file_name = 'results_16_1/from' + start_time_name + 'to' + end_time_name

    mask = (df['datetime'] > start_time) & (df['datetime'] <= end_time)
    df = df.loc[mask]
    
    name_data = file_name + '.xlsx'   
    df.to_excel(name_data)
    
    mask = (df['monitor_status'] == 1)
    df = df.loc[mask]
    
    df.to_excel(name_data)
    
    c_list=['C1', 'C2', 'C3', 'C4']
    d_list = ['D1', 'D2', 'D3', 'D4']
    
    for name_c in c_list:
        #name = name
        globals()[name_c] = df.loc[df['name'] == name_c]
        #globals()[name] = globals()[name].set_index('datetime').resample('1h').mean()
        globals()[name_c] = globals()[name_c].set_index('datetime').mean(axis = 0) 
        #globals()[name].insert(0, 'data_type', name)
    
    for name_d in d_list:
        globals()[name_d] = df.loc[df['name'] == name_d]
        #globals()[name] = globals()[name].set_index('datetime').resample('1h').sem()
        globals()[name_d] = globals()[name_d].set_index('datetime').mean(axis = 0)
        #globals()[name].insert(0, 'data_type', name)
    
    df_result = pd.concat([C1, C2, C3, C4, D1, D2, D3, D4], axis=1)
    
    df_result = df_result.rename(columns={0: 'C1', 1: 'C2', 2: "C3", 3: "C4", 4: "D1", 5: "D2", 6: "D3", 7: "D4"})
    
    name_mean = file_name + '_mean' + '.xlsx'
    df_result.to_excel(name_mean)
    
    c_list=['C1', 'C2', 'C3', 'C4']
    d_list = ['D1', 'D2', 'D3', 'D4']
    
    for name in c_list:
        #name = name
        globals()[name] = df.loc[df['name'] == name]
        #globals()[name] = globals()[name].set_index('datetime').resample('1h').mean()
        globals()[name] = globals()[name].set_index('datetime').sem(axis = 0) 
        #globals()[name].insert(0, 'data_type', name)
    
    for name in d_list:
        globals()[name] = df.loc[df['name'] == name]
        #globals()[name] = globals()[name].set_index('datetime').resample('1h').sem()
        globals()[name] = globals()[name].set_index('datetime').sem(axis = 0)
        #globals()[name].insert(0, 'data_type', name)
    
    
    df_result = pd.concat([C1, C2, C3, C4, D1, D2, D3, D4], axis=1)
    
    df_result = df_result.rename(columns={0: 'C1', 1: 'C2', 2: "C3", 3: "C4", 4: "D1", 5: "D2", 6: "D3", 7: "D4"})
    
    name_sem = file_name + '_sem' + '.xlsx'
    df_result.to_excel(name_sem)
    
    
name = 'data/franka_data04_13_11'+'.xlsx'
#df = pd.read_excel(name, sep='\t', index_col=0)

lista = [['2019-11-04 12:00:00', '2019-11-05 08:00:00'],
         ['2019-11-05 12:00:00', '2019-11-06 08:00:00'],
         ['2019-11-06 12:00:00', '2019-11-07 08:00:00'],
         ['2019-11-07 12:00:00', '2019-11-08 08:00:00'],
         ['2019-11-08 12:00:00', '2019-11-09 08:00:00'],
         ['2019-11-09 12:00:00', '2019-11-10 08:00:00'],
         ['2019-11-10 12:00:00', '2019-11-11 08:00:00'],
         ['2019-11-11 12:00:00', '2019-11-12 08:00:00'],
         ['2019-11-12 12:00:00', '2019-11-13 08:00:00']]

for element in lista:
    start_time = element[0]
    end_time = element[1]
    create_xlsx(df, start_time, end_time)

