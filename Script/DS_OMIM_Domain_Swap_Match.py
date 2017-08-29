#!/usr/bin/python
import re

Path = '/home/pankaj/NCBS_2017_Domain_Swapping/Data/'
File_names = ['Domain_swap_Uniprot_IDs']

for current_file in File_names:
	input_file = ''.join([Path, 'Processed_Data/', current_file, '.txt'])
	Gene_Dict = {}
	with open(input_file, 'r') as f:
		for line in f.readlines()[1:]:
			line = line.strip('\n')
			line = line.split('\t')
			ID = line[1]
			Gene_Dict[ID] = line[0]

	input_file2 = ''.join([Path, 'Raw_Data/', 'Mouse_Heart_Development', '.csv'])
	output = ''
	with open(input_file2,'r') as f2:
		for line in f2.readlines():
			line = line.strip('\n')
			Gene = line
			try:
				Uniprot = Gene_Dict[Gene]
				output += Gene + '\t' + Uniprot + '\n'
			except Exception as e:
			 	pass
	output_file = ''.join([Path, 'Result/','Cardio_Domain_Swap_Mouse_Genes','.txt'])
	with open(output_file, 'w') as fout:
		fout.write(output) 


#!/usr/bin/python
import os
import argparse

def main( ):

    	input_file = args_.input_argument
	input2_file = args_.input2_argument
 	output_file = args_.output_argument

	if os.path.exists(output_file):
		print('output file already present. Are you sure to overwrite? \n If yes then please delete the original file') 
		exit()

	Gene_Dict = {}
	with open(input_file, 'r') as f:
		for line in f.readlines()[1:]:
			line = line.strip('\n')
			line = line.split('\t')
			ID = line[1]
			Gene_Dict[ID] = line[0]

	output = ''	
	with open(input2_file,'r') as f2:
		for line in f2.readlines():
			line = line.strip('\n')
			Gene = line
			try:
				Uniprot = Gene_Dict[Gene]
				output += Gene + '\t' + Uniprot + '\n'
			except Exception as e:
			 	pass

	with open(output_file, "w" ) as fout: 
		fout.write(output)


if __name__ == "__main__":

    	parser = argparse.ArgumentParser(description="A script to extract Cardiomyopathy genes from OMIM data")
    	parser.add_argument('-i', dest="input_argument", default="Data/Raw_Data/DS_OMIM_Cardio_Genes_Data.txt", help="Check Raw_Data folder and README for correct name")
	parser.add_argument('-i2', dest="input2_argument", default="Data/Raw_Data/DS_OMIM_Cardio_Genes_Data.txt", help="Check Raw_Data folder and README for correct name")
	parser.add_argument('-o', dest="output_argument", default="Data/Processed_Data/DS_Extracted_Cardio_Genes_OMIM.txt", help="Put output in Processed_Data folder ")
     	args_ = parser.parse_args()
    	main(  )
    	print( '[INFO] All done' )	

