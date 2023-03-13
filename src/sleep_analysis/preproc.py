# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 01:13:06 2020

@author: icecream_boi

"""
import pandas as pd 

def clear_data(df):
    """loads and clears data, Returns cleared dataframe, removing 
    notneeded columns"""
    
    df['datetime'] = df.iloc[:, 0] + ' ' + df.iloc[:, 1]
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    df = df.set_index(df['datetime'])
    
    df.drop(df.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8]], axis = 1, inplace = True) 
    df = df.drop(columns=['datetime'])
    
    columns = list(range(1, len(df.columns)+1))
    df.columns = columns
    
    return df

path = r'F:\0_theory\biotech_data\sleep_analysis\raw_data\oxmutCtM003.txt'
df = pd.read_csv(path, index_col=0, sep='\t', header=None)
df = clear_data(df)
df_pop1 = df.loc[:, :13]
df_pop2 = df.loc[:, 17:]
df_pop1.to_csv('results/Elav-SOD3.csv')
df_pop2.to_csv('results/DDC-SOD3.csv')

path = r'F:\0_theory\biotech_data\sleep_analysis\raw_data\oxmutCtM004.txt'
df = pd.read_csv(path, index_col=0, sep='\t', header=None)
df = clear_data(df)
df_pop1 = df.loc[:, :6]
df_pop2 = df.loc[:, 17:21]
df_pop1.to_csv('results/DDC-SOD2.csv')
df_pop2.to_csv('results/Elav-SOD1.csv')

path = r'F:\0_theory\biotech_data\sleep_analysis\raw_data\oxmutCtM005.txt'
df = pd.read_csv(path, index_col=0, sep='\t', header=None)
df = clear_data(df)
df_pop1 = df.loc[:, :16]
df_pop2 = df.loc[:, 17:]
df_pop1.to_csv('results/Elav-Gal4.csv')
df_pop2.to_csv('results/DDC-Gal4.csv')

path = r'F:\0_theory\biotech_data\sleep_analysis\raw_data\oxmutCtM006.txt'
df = pd.read_csv(path, index_col=0, sep='\t', header=None)
df = clear_data(df)
df_pop1 = df.loc[:, :16]
df_pop1.to_csv('results/CS-Ch.csv')



