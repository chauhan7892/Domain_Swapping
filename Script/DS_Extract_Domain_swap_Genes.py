#!/usr/bin/python
import os
import argparse

args_ = None

def main( ):

    	input_file = args_.input_argument
 	output_file = args_.output_argument

	if os.path.exists(output_file):
		print('output file already present. Are you sure to overwrite? \n If yes then please delete the original file') 
		exit()

	with open(input_file,'r') as f:
		temp = []
		for line in f.readlines()[1:]:
			line = line.strip('\n')
			line = line.split('\t')
			gene = line[12].split(';')
			temp += gene

		output = ''
		for genes in temp:
			if genes not in output:
				output += genes + '\n'

	with open(output_file, "w" ) as fout: 
		fout.write(output)


if __name__ == "__main__":

    	parser = argparse.ArgumentParser(description="A script to extract domain swapping genes from data")
    	parser.add_argument('-i', dest="input_argument", default="Data/Raw_Data/Domain_swapping_Data.csv", help="Check Raw_Data folder and README for correct name")
	parser.add_argument('-o', dest="output_argument", default="Data/Processed_Data/Extracted_Domain_swapping_genes.txt", help="Put output in Processed_Data folder ")
     	args_ = parser.parse_args()
    	main(  )
    	print( '[INFO] All done' )	
