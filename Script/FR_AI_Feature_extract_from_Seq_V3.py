import sys, re, argparse
import FR_Protein_Feature_extract_V2 as ProtFEAT
import collections

args_ = None

def add_aa_index_features(seq_feature_dict,feature_dict,seq,seq_id) :
	for feat_id in feature_dict :
		seq_feature_dict[seq_id][feat_id] = 0
		cnt_val_error = 0 # count illegal amino acids
		val = 0
		for aa in seq :
			if aa not in feature_dict[feat_id]:
				cnt_val_error += 1
				continue
			val_str = feature_dict[feat_id][aa]
			try:
				val += float(val_str)
			except ValueError:
				cnt_val_error += 1
		seq_feature_dict[seq_id][feat_id] = val/(len(seq)-cnt_val_error)

def add_special_features(seq_feature_dict,feature_dict,seq,seq_id) :
    aa_freq_dict =  ProtFEAT.Get_AA_percentage(seq)

    res = ProtFEAT.Small_seq(aa_freq_dict)
    for feat_id in res :
        seq_feature_dict[seq_id][feat_id] = res[feat_id]

    res = ProtFEAT.charge_seq(aa_freq_dict)
    for feat_id in res :
        seq_feature_dict[seq_id][feat_id] = res[feat_id]

    res = ProtFEAT.functional_group(aa_freq_dict)
    for feat_id in res :
        seq_feature_dict[seq_id][feat_id] = res[feat_id]

    res = ProtFEAT.Hydrophobicity(aa_freq_dict)
    for feat_id in res :
        seq_feature_dict[seq_id][feat_id] = res[feat_id]

    res = ProtFEAT.Aromaticity(aa_freq_dict)
    for feat_id in res :
        seq_feature_dict[seq_id][feat_id] = res[feat_id]

    res = ProtFEAT.sec_struct_frac(aa_freq_dict)
    for feat_id in res :
        seq_feature_dict[seq_id][feat_id] = res[feat_id]

    res = ProtFEAT.pI(seq)
    for feat_id in res :
        seq_feature_dict[seq_id][feat_id] = res[feat_id]

    for aa in aa_freq_dict :
        feat_id = 'Freq_' + aa
        seq_feature_dict[seq_id][feat_id] = aa_freq_dict[aa]



def main( ):

    input_file = args_.input_argument
    output_file = args_.output_argument

    feat_list = []
    feature_dict = {}
    res_list = []
    firstLine = True

    with open( input_file[0], 'r' ) as f1: # Feature list file
        for line in f1:
            feat_ID = line.strip().split(' ')[0]
            feat_list.append(feat_ID)


    with open( input_file[1], 'r' ) as f2: # AAIndex file
        for line in f2:
            if firstLine == True:
                items = line.strip().split('\t')
                for item in items:
                    res_list.append(item)
                firstLine = False
            else :
                items = line.strip().split('\t')
                pos = 1
                feat_id = items[0]
                if feat_id in feat_list:
                    feature_dict[feat_id] = {}
                    for item in items[1:]:
                        feature_dict[feat_id][res_list[pos]] = item
                        pos += 1


                        seq_feature_dict = collections.OrderedDict()
    with open(input_file[2], 'r') as f3: # sequence file
        seq = ""
        for line in f3:
            line = line.strip()
            if re.match('>',line) :
                if seq != "" :
                    add_aa_index_features(seq_feature_dict,feature_dict,seq,seq_id)
                    add_special_features(seq_feature_dict,feature_dict,seq,seq_id)
                    seq = ""
                seq_id = line.split('>')[1].split(' ')[0]
                seq_feature_dict[seq_id] = collections.OrderedDict()
                continue
            else :
                seq += line
    	if seq != "" :
            add_aa_index_features(seq_feature_dict,feature_dict,seq,seq_id)
            add_special_features(seq_feature_dict,feature_dict,seq,seq_id)
    out_str = ''
    for feature_id in seq_feature_dict[seq_id] :
        out_str += '\t' + feature_id
    out_str += '\n'
    for seq_id in seq_feature_dict :
        out_str += seq_id
        for feature_id in seq_feature_dict[seq_id] :
        	out_str+= "\t" + str(seq_feature_dict[seq_id][feature_id])
        out_str += '\n'


    with open(output_file[0],'w') as f_out:
        f_out.write(out_str)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A script to output features from processed AAIndex database file")
    parser.add_argument('-i', nargs='+', dest="input_argument", default="Data/Processed_Data/AI_AAIndex_features_for_use.txt", help="Check Procesed_Data folder and README for correct name")
    parser.add_argument('-o', nargs='+', dest="output_argument", default="Data/Processed_Data/SR_Test_negative_features.dat", help="Put output in Processed_Data folder ")
    args_ = parser.parse_args()
    main(  )
    print( '[INFO] All done' )
