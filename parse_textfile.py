__author__ = 'brendan'

import os
import pandas as pd
import datetime

def run(textfile_name, hours_behind_UTC):

    """
    :param textfile_name: name of text file to be parsed
    :return:

    """
    wd = os.getcwd()
    textfile_path = wd + r'\Text Files\%s'%textfile_name
    temp_scaling_factor = 10.

    result_dataframe = pd.DataFrame(columns=['UCT Datetime', 'Custom Datetime', 'UCT Date', 'Custom Date', 'Temp (C)'])

    with open(textfile_path) as textfile:

        whole_textfile_string = textfile.read()

        textfile_by_row = whole_textfile_string.rsplit('\n')[:-1]
        num_rows = len(textfile_by_row)

        row_num = 0
        for row in textfile_by_row:
            UTC_year, UTC_month, UTC_day, UTC_hour, UTC_minute = int(row[15:19]), int(row[19:21]), int(row[21:23]), int(row[23:25]), int(row[25:27])

            UTC_datetime = datetime.datetime.combine( datetime.date(UTC_year,UTC_month,UTC_day),
                                         datetime.time(UTC_hour,UTC_minute)
                                        )

            if UTC_datetime.time() < datetime.time(hours_behind_UTC,0):
                Custom_datetime = UTC_datetime - datetime.timedelta(1) + datetime.timedelta(hours=24-hours_behind_UTC)
            else:
                Custom_datetime = UTC_datetime - datetime.timedelta(hours=hours_behind_UTC)

            excel_utc_datetime = UTC_datetime.strftime('%x %X')
            excel_Custom_datetime = Custom_datetime.strftime('%x %X')

            row_temp = int(row[87:92])/temp_scaling_factor if row[87:92] != '+9999' else '#N/A'

            result_dataframe.loc[row_num] = [UTC_datetime,Custom_datetime,excel_utc_datetime,excel_Custom_datetime,row_temp]

            if row_num%1000 == 0:
                print 'Row %s of %s parsed. (%s %%)'%(row_num,num_rows,str(100*float(row_num)/float(num_rows))[:5])
            row_num += 1

        textfile.close()

    result_dataframe.to_csv(path_or_buf= wd + r'\Parsed Files' + r'\%s_parsed.csv'%textfile_name[:-4],columns=['UCT Date','Custom Date', 'Temp (C)'])

    return result_dataframe
