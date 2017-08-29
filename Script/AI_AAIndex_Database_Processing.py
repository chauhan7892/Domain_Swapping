
import os
import argparse

args_ = None

def main( ):

    input_file = args_.input_argument
    	output_file = args_.output_argument

    if os.path.exists(output_file):
    	print('output file already present. Are you sure to overwrite? \n If yes then please delete the original file')
    	exit()

    All_features_info = ''
    Feature_list = ''
    with open(input_file,'r') as f:
        for line in f:
    		line = ' '.join(line.split())
    		if line[0] == 'H' and line[1] == ' ':
    			ID = line.split(' ')[1]
    			All_features_info = All_features_info + ID + '\t'

            if not Feature_list and line[0] == 'I' and line[1] == ' ':
            	AA_names = line.strip('I ').split(' ')
            	AA_upper_layer = []
            	AA_lower_layer = []
            	for item in AA_names:
                    splitted_AAs = item.split('/')
                    AA_upper_layer.append(splitted_AAs[0])
                    AA_lower_layer.append(splitted_AAs[1])
                next_line = next(f)
                next_line = ' '.join(next_line.split())
                feature_line1 = next_line.split(' ')

                next_second_line = next(f)
                next_second_line = ' '.join(next_second_line.split())
                feature_line2 = next_line.split(' ')

                Feature_list = 'Feature_ID\t' + ('\t').join(AA_upper_layer) + '\t' + ('\t').join(AA_lower_layer) + '\n'
                All_features_info = Feature_list + All_features_info + ('\t').join(feature_line1) + '\t' + ('\t').join(feature_line2) + '\n'

            elif line[0] == 'I' and line[1] == ' ':
                next_line = next(f)
                next_line = ' '.join(next_line.split())
                feature_line1 = next_line.split(' ')
                next_second_line = next(f)
                next_second_line = ' '.join(next_second_line.split())
                feature_line2 = next_line.split(' ')

                All_features_info = All_features_info + ('\t').join(feature_line1) + '\t' + ('\t').join(feature_line2) + '\n'


	with open (output_file, 'w') as fout:
		fout.write(All_features_info)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="A script to process features from AAIndex database aaindex1 file")
	parser.add_argument('-i', dest="input_argument", default="Data/Raw_Data/AAIndex_database_features_data.txt", help="Check Raw_Data folder and README for correct name")
    parser.add_argument('-o', dest="output_argument", default="Data/Processed_Data/Processed_AAIndex_features.dat", help="Put output in Processed_Data folder ")
 	args_ = parser.parse_args()
	main(  )
    print( '[INFO] All done' )
