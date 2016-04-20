__author__ = 'brendan'

import datetime
import pandas as pd
import parse_textfile
import os

def run(filename,input_dataframe=None,
        start_year=2010,start_month=1,start_day=1,start_hour=0,start_minute=0,frequency='H',num_periods=8760,
        parsed_file_path=None, output_path=None):
    """
    Takes a timeseries of temperature data and maps it to a prescribed timeseries, via the following rule:
        -Use the most recent EARLIER point in time that has a numeric value

    :param filename: initial filename to be timestepped
    :param input_dataframe: dataframe that results from parse_textfile, if it exists
        -If not, it will be re-created from the appropriate CSV
    :param start_year, start_month, start_day, start_hour, start_minute: Used to create the beginning of the timestep series we wish to match to
    :param frequency: the size of each timestep
    :param num_periods: the length of the entire timestep series
    """

    wd = os.getcwd()
    if output_path == None:
        output_path = wd + r'\Timestep Files'

    WBAN_ID = filename.rsplit('-')[1]
    output_filename = '%s_%s-%s-%s_freq%s_n%s'%(WBAN_ID,start_year,start_month,start_day,frequency,num_periods)
    if output_filename in os.listdir(output_path):
        print "File already created."
        exit()

    else:
        print "Timestep file not detected."

        #Create our output dataframe
        start_datetime = datetime.datetime.combine(datetime.date(start_year,start_month,start_day),
                                                   datetime.time(start_hour,start_minute))
        datetimes = pd.date_range(start_datetime,freq=frequency,periods=num_periods)
        timestep_df = pd.DataFrame(index=datetimes,columns=['Actual Time Used', 'Temp (C)'])


        if input_dataframe == None:
            print '...Building dataframe from parsed CSV...'
            input_dataframe = CreateDataframeFromParsedfile(filename,parsed_file_path)


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

        timestep_df.to_csv(path_or_buf= output_path + r'\%s.csv'%output_filename,
                           columns=['Actual Time Used', 'Temp (C)'])

        return timestep_df

def CreateDataframeFromParsedfile(filename,Parsedfile_path=None):
    """
    Rebuilds a dataframe similar to the one output by parse_textfile, using the CSV that is output from the function
    """
    wd = os.getcwd()

    if Parsedfile_path == None:
        parsed_file_path = wd + r'\Parsed Files'
    else:
        parsed_file_path = Parsedfile_path

    parsed_file_as_DF = pd.DataFrame.from_csv(parsed_file_path + r'\%s_parsed.csv'%filename)

    for index in parsed_file_as_DF.index:
        UCT_date_as_string = parsed_file_as_DF.loc[index]['UCT Date']
        Custom_date_as_string = parsed_file_as_DF.loc[index]['Custom Date']

        parsed_file_as_DF.loc[index,'UCT Datetime'] = datetime.datetime.strptime(UCT_date_as_string,'%m/%d/%y %H:%M:%S')
        parsed_file_as_DF.loc[index,'Custom Datetime'] = datetime.datetime.strptime(Custom_date_as_string,'%m/%d/%y %H:%M:%S')

    return parsed_file_as_DF