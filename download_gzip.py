__author__ = 'brendan'

import os
import time

def run(data_string,output_path=None):
    """
    # http://www1.ncdc.noaa.gov/pub/data/noaa/2010/010010-99999-2010.gz

    :param data_string:
    :param output_path:
    :return:
    """

    if output_path == None:
        output_path = os.getcwd() + r'\ZipFiles'

    filename = '%s.gz'%data_string
    name_of_output_file = output_path + r'\%s.gz'%data_string

    if filename in os.listdir(output_path):
        print 'Zip file already downloaded.'

    else:
        data_year = data_string.rsplit('-')[2]
        url = 'http://www1.ncdc.noaa.gov/pub/data/noaa/%s/%s.gz'%(data_year,data_string)

        os_string = 'C:/Users/brendan/Downloads/curl-7.38.0-win64/bin/curl ' + '\"' + url + '\"' + ' > '
        os.system( os_string + name_of_output_file )