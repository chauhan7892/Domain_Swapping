#!usr/bin/python
import sys, os, subprocess
from datetime import datetime

args_ = None

def main( ):

    input_file = args_.input_argument
    output_file = args_.output_argument

    #Date = str(datetime.now())
    User = ''.join(['Personnel: ', 'Pankaj Chauhan'])
    Date_current = ''.join(['Date: ', str(datetime.now())])
    Separatrix = '*****************************\n'
    Word1 = 'Aim: '
    Word2 = 'Url/Source: '
    Separatrix2 = '-----------------------------\n'

    if not os.path.exists(input_file):
        print('Input file not found. Please check the input again.')
        exit()

    if not os.path.exists(output_file):
        print('Output file not found. Please check the output again.')
        exit()

    indexed_files = []
    f_in = open(input_file,'r')

    for line in f_in.readlines()[7:]:
        if line:
            line = line.strip('\n')
            indexed_files.append(line)
    f_in.close()

    f_in_append = open(input_file, 'a')
    new_file = ''

    f_out_append = open(output_file, 'a')
    output_description = ''

    path = './Data/Raw_Data/'
    stripped_input = input_file.split('/')[-1]
    stripped_output = output_file.split('/')[-1]

    for dir_Name, _, files in os.walk(path):
        for file_Name in files:
            if (file_Name not in indexed_files) and (file_Name != stripped_input) and (file_Name != stripped_output):
                new_file = new_file + str(file_Name) + '\n'
                file_path = dir_Name + '/' + file_Name
                Date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                Date_stamping = ''.join(['Date: ', str(Date)])
                output_description += ( '\n' + Separatrix + '\n ' + Date_stamping + '\n' + str(file_Name) + '\n \n' + Word1  + '\n' + Word2 + '\n' + Separatrix2)

    f_out_append.write(output_description)
    f_out_append.close()

    f_in_append.write(new_file)
    f_in_append.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="A script to document Raw Data")
    parser.add_argument('-i', dest="input_argument",default="temp_log.txt", help="Raw_Data_documentation")
    parser.add_argument('-o', dest="output_argument",default="temp_README.txt", help="Raw_Data_documentation")
    args_ = parser.parse_args()
    print( 'done' )

    main(  )
