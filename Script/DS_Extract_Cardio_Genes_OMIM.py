#!/usr/bin/python
import os
import argparse

def main( ):

    	input_file = args_.input_argument
 	output_file = args_.output_argument

	if os.path.exists(output_file):
		print('output file already present. Are you sure to overwrite? \n If yes then please delete the original file') 
		exit()

	with open(input_file,'r') as f:
		temp = []
		for line in f.readlines()[11:]:
			line = line.strip('\n').replace(' ', '')
			line = line.split('\t')
			gene = line[2].split(',')
			temp += gene

		output = ''
		for genes in temp:
			if genes not in output:
				output += genes + '\n'

	with open(output_file, "w" ) as fout: 
		fout.write(output)


if __name__ == "__main__":

    	parser = argparse.ArgumentParser(description="A script to extract Cardiomyopathy genes from OMIM data")
    	parser.add_argument('-i', dest="input_argument", default="Data/Raw_Data/DS_OMIM_Cardio_Genes_Data.txt", help="Check Raw_Data folder and README for correct name")
	parser.add_argument('-o', dest="output_argument", default="Data/Processed_Data/DS_Extracted_Cardio_Genes_OMIM.txt", help="Put output in Processed_Data folder ")
     	args_ = parser.parse_args()
    	main(  )
    	print( '[INFO] All done' )	

