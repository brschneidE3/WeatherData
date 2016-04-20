__author__ = 'brendan'

import parse_textfile
import parsed_to_timestep
import zip_to_txt
import time
import download_gzip

#Inputs:
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

list_of_filestrings = ['722900-23188-2010',
                        '723805-23179-2010']
"""
list_of_filestrings = ['010010-99999-2010']
HoursBehindUTC = 8

#main:
start = time.time()
for filename in list_of_filestrings:
    # (0) TODO: download zip file solely from text string
    # http://www1.ncdc.noaa.gov/pub/data/noaa/2014/010100-99999-2014.gz
    download_gzip.run(filename)

    # (1) Convert gzip file to txt file
    zip_to_txt.run(filename)

    # (2) Convert txt file to parsed csv & dataframe
    data_frame = parse_textfile.run(filename,HoursBehindUTC)

    # (3) Convert parsed dataframe to specified timeframe CSV
    parsed_to_timestep.run(filename,data_frame)
end = time.time()
elapsed = end - start
print 'Timestepping program took %s sec (%s min) to run.'%(elapsed,elapsed/60)