import os
import pandas as pd 
import matplotlib.pyplot as plt

path = r'F:\0_theory\biotech_data\sleep_analysis\results'
files = {}
for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.update({file[:-4] : os.path.join(r, file)})
  
                           
for pop_name, path in files.items():   
    df = pd.read_csv(path, index_col='datetime')
    
    df_proc = df
    result_table = pd.DataFrame()
    
    while len(df_proc) > 0:
        selected_rows = df_proc.iloc[:5]
        
        selected_rows_time = list(selected_rows.index)
        
        result = selected_rows.mean(axis=0)
        result = pd.DataFrame(result)
        result.columns = selected_rows_time[0].split(';')

        result_table = pd.concat([result_table, result], axis=1)
        
        df_proc = df_proc.iloc[5:]
    
    result_table = result_table.T
    result_table.to_csv('sleep_fixed/' + pop_name + '.csv')    
    
    
    df.index = pd.to_datetime(df.index)
    df = df.groupby([df.index.hour,
                     df.index.minute]).mean().mean(axis=1)
    
    ax = df.plot.line(title=pop_name)
    plt.show()

    



"""
draw = ['Elav-SOD3, Elav-SOD1, Elav-Gal4, CS',
        'DDC-SOD3, DDC-SOD2, DDC-Gal4, CS',
        'DDC-SOD3, Elav-SOD3, CS']
"""

