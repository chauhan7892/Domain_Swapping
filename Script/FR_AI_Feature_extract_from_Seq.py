import sys, re, argparse

args_ = None

def main( ):

    input1_file = args_.input1_argument
    input2_file = args_.input2_argument
    output_file = args_.output_argument

    feature_dict = {}
    res_list = []
    firstLine = True

    with open( input1_file, 'r' ) as f1:
        for line in f1:
            if firstLine == True:
                items = line.strip().split('\t')
                for item in items:
                    res_list.append(item)
                firstLine = False
            else :
                items = line.strip().split('\t')
                pos = 1
                feat_id = items[0]
                feature_dict[feat_id] = {}
                for item in items[1:]:
                    feature_dict[feat_id][res_list[pos]] = item
                    pos += 1

    seq_feature_dict = {}

    with open(input2_file, 'r') as f2:
        seq = ""
        for line in f2:
            line = line.strip()
            if re.match('>',line) :
                if seq != "" :
                    for feat_id in feature_dict :
                        seq_feature_dict[seq_id][feat_id] = 0
                        cnt_val_error = 0
                        val = 0
                        for aa in seq :
                            if aa not in feature_dict[feat_id] :
                                cnt_val_error += 1
                                continue
                            val_str = feature_dict[feat_id][aa]
                            try:
                                val += float(val_str) # for int, long and float
                            except ValueError:
                                cnt_val_error += 1
                        #print len(seq),cnt_val_error
                        seq_feature_dict[seq_id][feat_id] = val/(len(seq)-cnt_val_error)
                    seq = ""
                seq_id = line.split('>')[1].split(' ')[0]
                seq_feature_dict[seq_id] = {}
                continue
            else :
                seq += line
    	if seq != "" :
    		for feat_id in feature_dict :
    			seq_feature_dict[seq_id][feat_id] = 0
    			cnt_val_error = 0
    			val = 0
    			for aa in seq :
    				if aa not in feature_dict[feat_id]:
    					cnt_val_error += 1
    					continue
    				val_str = feature_dict[feat_id][aa]
    				try:
    					val += float(val_str) # for int, long and float
    				except ValueError:
    					cnt_val_error += 1
    			seq_feature_dict[seq_id][feat_id] = val/(len(seq)-cnt_val_error)

    out_str = ''
    for seq_id in seq_feature_dict :
        out_str += seq_id
        for feature_id in seq_feature_dict[seq_id] :
        	out_str+= "\t" + str(seq_feature_dict[seq_id][feature_id])
        out_str += '\n'

        
    with open(output_file,'w') as f_out:
        f_out.write(out_str)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A script to output features from processed AAIndex database file")
    parser.add_argument('-i1', dest="input1_argument", default="Data/Processed_Data/AAIndex_processed_data.txt", help="CheckProcesed_Data folder and README for correct name")
    parser.add_argument('-i2', dest="input2_argument", default="Data/Raw_Data/SR/SR_Test_negative.seq", help="CheckProcesed_Data folder and README for correct name")
    parser.add_argument('-o', dest="output_argument", default="Data/Processed_Data/SR_Test_negative_features.dat", help="Put output in Processed_Data folder ")
    args_ = parser.parse_args()
    main(  )
    print( '[INFO] All done' )
