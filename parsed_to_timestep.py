__author__ = 'brendan'

import datetime
import pandas as pd
import parse_textfile
import os

def run(filename,input_dataframe=None,start_year=2010,start_month=1,start_day=1,start_hour=0,start_minute=0,frequency='H',num_periods=8760):
    """
    :param dataframe: dataframe with integer indices and columns 'UCT Date', 'Custom Date', and 'Temp (C)'
    :return:
    """
    #TODO: have this recreate input dataframe from CSV

    wd = os.getcwd()

    start_datetime = datetime.datetime.combine(datetime.date(start_year,start_month,start_day),
                                               datetime.time(start_hour,start_minute))

    datetimes = pd.date_range(start_datetime,freq=frequency,periods=num_periods)

    timestep_df = pd.DataFrame(index=datetimes,columns=['Actual Time Used', 'Temp (C)'])

    timestep_counter = 0
    for timestep in timestep_df.index:

        greatest_earlier_timestep = max(input_dataframe[ input_dataframe['Custom Datetime'] <= timestep ]['Custom Datetime'])
        greatest_earlier_temp = max(input_dataframe[input_dataframe['Custom Datetime']==greatest_earlier_timestep]['Temp (C)'])

        while greatest_earlier_temp == '#N/A':
            greatest_earlier_timestep = max(input_dataframe[ input_dataframe['Custom Datetime'] < greatest_earlier_timestep ]['Custom Datetime'])
            greatest_earlier_temp = max(input_dataframe[input_dataframe['Custom Datetime']==greatest_earlier_timestep]['Temp (C)'])

        timestep_df.loc[timestep] = [greatest_earlier_timestep, greatest_earlier_temp]

        if timestep_counter%1000 == 0:
            print 'Corresponding temperature for timestep %s of %s found.'%(timestep_counter,num_periods)
        timestep_counter += 1

    unique_timesteps_used = float(len(timestep_df['Actual Time Used'].value_counts()))
    data_density_metric = unique_timesteps_used / num_periods
    timestep_df.loc['Unique Timesteps Used'] = [unique_timesteps_used, '']
    timestep_df.loc['Data Density'] = [data_density_metric, '']

    timestep_df.to_csv(path_or_buf= wd + r'\Timestep Files' + r'\%s_timestepped.csv'%filename,
                       columns=['Actual Time Used', 'Temp (C)'])

"""
list_of_filestrings = ['722868-93138-2010',
                       '722897-93206-2010',
                       '722907-53143-2010',
                       '722950-23174-2010',
                       '722977-93184-2010',
                       '723825-23131-2010',
                       '723940-23273-2010',
                       '724927-23285-2010',
                       '724930-23230-2010',
                       '724957-23213-2010',
                       '725910-24216-2010',
                       '725945-24283-2010']
"""
list_of_filestrings = ['722900-23188-2010',
                        '723805-23179-2010']

for filename in list_of_filestrings:
    try:
        data_frame = parse_textfile.run(filename + '.txt',8)
        run(filename,data_frame)
    except:
        continue

#data_frame = parse_textfile.run('724930-23230-2010.txt',8)
#run('724930-23230-2010',data_frame)