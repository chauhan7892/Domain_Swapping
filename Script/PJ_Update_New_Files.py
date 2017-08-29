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
	
	path = os.path.dirname(os.path.abspath(input_file))
	directory_files = os.listdir(path)
	
	f_in_append = open(input_file, 'a') 
	new_file = ''

	f_out_append = open(output_file, 'a')	
	output_description = ''

	for f_dir in directory_files:
		if (f_dir not in indexed_files):
		#if ((f_dir not in indexed_files) and (f_dir != input_file) and (f_dir != output_file)):
			new_file = new_file + str(f_dir) + '\n'		
			stamped_file = os.path.join(path, f_dir)
			Date = datetime.fromtimestamp(os.path.getmtime(stamped_file)).strftime('%Y-%m-%d %H:%M:%S')
			Date_stamping = ''.join(['Date: ', str(Date)]) 
			output_description += ( '\n' + Separatrix + '\n ' + Date_stamping + '\n' + str(f_dir) + '\n \n' + Word1  + '\n' + Word2 + '\n' + Separatrix2)	  

	
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
