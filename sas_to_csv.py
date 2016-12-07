"""
This program takes a directory as input and the looks for and converts sas 7 files (.sas7bdat) into csv files.
using pandas on this data was unsuccessful.
For each sas file found, the program will open a file with same base name and a .txt extension, loop through the sas
files one row at a time, and convert te list of fields into an output string to be written to the .txt file.

It will generate some basic statistics on the files in converts.
"""

import os
from sas7bdat import SAS7BDAT

in_path = "C:\\Temp\\finalproject\\sas_files"
out_path = "C:\\Temp\\finalproject\\text_files"
file_names = os.listdir(in_path)
for file_name in file_names:
    # print(file_name)
    if file_name.endswith('.sas7bdat'):
        # file_name = "nyts00fmts.sas7bcat"
        outfile_name = file_name.split('.')[0] + '.txt'
        print('outfile name: {}'.format(outfile_name))
        print('{} is a sas file'.format(file_name))
        with SAS7BDAT(os.path.join(in_path, file_name), encoding='latin-1') as infile:
            with open(os.path.join(out_path, outfile_name), 'w') as outfile:
                for line in infile:
                    outline = ''
                    for item in line:
                        if outline != '':
                            outline += ','

                        outline += str(item)
                    outline += '\n'
                    outfile.write(outline)
                # print(line)
