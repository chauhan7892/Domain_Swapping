import sys
import re
feature_dict = {}
res_list = []
firstLine = True
with open(sys.argv[1]) as f:
    for line in f:
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
with open(sys.argv[2]) as f:
    seq = ""
    for line in f:
        line = line.strip()
        #print line
        if re.match('>',line) :
            seq_id = line.split('>')[1].split(' ')[0]
            seq_feature_dict[seq_id] = {}
            if seq != "" :
                for feat_id in feature_dict :
                    seq_feature_dict[seq_id][feat_id] = 0
                    cnt_val_error = 0
                    val = 0
                    for aa in seq :
                        val_str = feature_dict[feat_id][aa]
                        try:
                            val += float(val_str) # for int, long and float
                        except ValueError:
                            cnt_val_error += 1
                    #print len(seq),cnt_val_error
                    seq_feature_dict[seq_id][feat_id] = val/(len(seq)-cnt_val_error)
                seq = ""
            continue
        else :
            seq += line
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
            seq_feature_dict[seq_id][feat_id] = val/(len(seq)-cnt_val_error)

for seq_id in seq_feature_dict :
    print seq_id
    print seq_feature_dict[seq_id]
