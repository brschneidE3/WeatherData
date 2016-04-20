__author__ = 'brendan'

import gzip
import os

def run(gzip_filename,gzip_directory=None,txtFile_directory=None):

    """
    Takes in the name of a gzip file and rewrites contents of corresponding gzip file to a txt file
    """

    wd = os.getcwd()
    if gzip_directory == None:
        gzipFile_path = wd + r'\Zip Files'
    else:
        gzipFile_path = gzip_directory
    if txtFile_directory == None:
        txtFile_path = wd + r'\Text Files'
    else:
        txtFile_path = txtFile_directory

    ExistingTextFiles = os.listdir(txtFile_path)
    if gzip_filename + '.txt' in ExistingTextFiles:
        print 'Text file already created.'
    else:
        with gzip.open(gzipFile_path + r'\%s.gz'%gzip_filename,'rb') as gzip_file:
            file_content = gzip_file.read()
            gzip_file.close()

        with open(txtFile_path + r'\%s.txt'%gzip_filename,'w') as txt_file:
            txt_file.write(file_content)
            txt_file.close()
