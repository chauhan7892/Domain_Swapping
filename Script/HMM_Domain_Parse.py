#!/usr/bin/env python

import re,glob
import sys
from collections import defaultdict
from operator import itemgetter
#from collections import Counter

args_ = None

def main( ):
    out_fd = open( args_.pfamda, "w" )
    uf = open( args_.uniqueDA, "w" )
    da_fd = open( args_.domain, "w" )

    #gid_dict = defaultdict( list )
    gid_dict={}
    domain_arch_dict={}

    with open( args_.hmmout, 'r' ) as f :
        for hmm_line  in f :
            if (re.match('#',hmm_line)) :
                continue
            hmm_cols = hmm_line.split()
            query_name = hmm_cols[3]
            #print query_name
            gid = query_name.split('|')[1]
            pfam_accession_desc = hmm_cols[0]
            pfam_id = hmm_cols[1]
            hmm_len = int(hmm_cols[2])
            qlen = int(hmm_cols[5])
            i_evalue = float(hmm_cols[12])
            env_cord_from = int(hmm_cols[19])
            env_cord_to = int(hmm_cols[20])
            hmm_cord_from = int(hmm_cols[15])
            hmm_cord_to = int(hmm_cols[16])
            target_cov = float((hmm_cord_to - hmm_cord_from))/float(hmm_len)
            #pfam_id = pfam_accession_id
            #print pfam_id
            pfam_item=[pfam_id,pfam_accession_desc,hmm_len,env_cord_from,env_cord_to,hmm_cord_from,hmm_cord_to,target_cov,qlen,i_evalue]
            #print pfam_item
            if (gid not in gid_dict) :
                gid_dict[gid] = {}
            if pfam_id not in gid_dict[gid] :                    
                gid_dict[gid][pfam_id] = []
                gid_dict[gid][pfam_id].append(pfam_item)
            else :
                gid_dict[gid][pfam_id].append(pfam_item)
        #print gid_dict     
    for gid in gid_dict :
        pfamda_txt = ""
        for pfam_id in gid_dict[gid] :
            gid_dict[gid][pfam_id] = sorted(gid_dict[gid][pfam_id], key=itemgetter(3))
            #print gid_dict
        coverage_list = []
        pfam_id_list = [] #Needed for Output DA file
        for pfam_id in gid_dict[gid] :
            #sorted(gid_dict[gid][pfam_id], key=itemgetter(2))
            for pfam_item in list(gid_dict[gid][pfam_id]) :
                if pfam_item[7] >= 0.7 and pfam_item[9] <= 1:
                    gid_dict[gid][pfam_id].remove(pfam_item)
                    coverage_list.append([pfam_item[2],pfam_item[3]])
                    pfamda_txt += "%s %s %s %s %s %s %s %s %.2f %s %s\n"%(gid,pfam_item[0],pfam_item[1],pfam_item[2],pfam_item[3],pfam_item[4],pfam_item[5],pfam_item[6],pfam_item[7],pfam_item[8],pfam_item[9] )
                    pfam_id_list.append([pfam_id,pfam_item[1],pfam_item[3],pfam_item[4],pfam_item[8],pfam_item[9]])
                    #print pfam_id_list
            stretch_found = True
            for pfam_item in list(gid_dict[gid][pfam_id]):
                if stretch_found :
                    prev_pfam_item = pfam_item
                    stretch_found = False
                    continue
                env_start1 = prev_pfam_item[3]
                env_start2 = pfam_item[3]
                env_end1 = prev_pfam_item[4]
                env_end2 = pfam_item[4]

                if pfam_item[5] > prev_pfam_item[5]:
                    hmm_start1 = prev_pfam_item[5]
                    hmm_start2 = pfam_item[5]
                    hmm_end1 = prev_pfam_item[6]
                    hmm_end2 = pfam_item[6]
                    env_start1 = prev_pfam_item[3]
                    env_start2 = pfam_item[3]
                    env_end1 = prev_pfam_item[4]
                    env_end2 = pfam_item[4]
                    i_evalue1 = prev_pfam_item[9]
                    i_evalue2 = pfam_item[9]
                    qcov1 = prev_pfam_item[7]
                    qcov2 = pfam_item[7]
                    pfam_accession_desc1 = prev_pfam_item[1]
                    pfam_accession_desc2 = pfam_item[1]
                    
                else :
                    hmm_start2 = prev_pfam_item[5]
                    hmm_start1 = pfam_item[5]
                    hmm_end2 = prev_pfam_item[6]
                    hmm_end1 = pfam_item[6]
                    env_start2 = prev_pfam_item[3]
                    env_start1 = pfam_item[3]
                    env_end2 = prev_pfam_item[4]
                    env_end1 = pfam_item[4]
                    i_evalue1 = pfam_item[9]
                    i_evalue2 = prev_pfam_item[9]
                    qcov1 = pfam_item[7]
                    qcov2 = prev_pfam_item[7]
                    pfam_accession_desc1 = pfam_item[1]
                    pfam_accession_desc2 = prev_pfam_item[1]


                hmm_len = pfam_item[2]
                #Proper continous
                proper_continous = False
                sign=""
                if (qcov1 < 0.7 and qcov2 < 0.7 and ((env_start2 <= env_end1 and env_end2 > env_end1 and hmm_start2 <= hmm_end1 and hmm_end2 > hmm_end1)
                    or (env_start2 <= env_end1 and env_end2 > env_end1 and hmm_start2 - hmm_end1 >= 0 and hmm_start2 - hmm_end1 < 25))):
                    target_cov = float((hmm_end2 - hmm_start1 + 1))/float(hmm_len)
                    proper_continous = True
                    sign="***"
                #Im Proper continous
                elif (qcov1 < 0.7 and qcov2 < 0.7 and env_start2 - env_end1 >= 0 and env_start2 - env_end1  < 25 and hmm_start2 - hmm_end1 >= 0 and hmm_start2 - hmm_end1 < 25 ):
                    target_cov = prev_pfam_item[7] + pfam_item[7]
                    sign="+++"
                #Discontinous   
                #elif (hmm_start2 - hmm_end1 > 0 and hmm_start2 - hmm_end1 < 25 and hmm_end2 > hmm_end1 ) :
                elif (qcov1 < 0.7 and qcov2 < 0.7 and env_start2 > env_start1 and env_end2 > env_end1 and hmm_start2 - hmm_end1 >= 0 and hmm_start2 - hmm_end1 < 25):
                    target_cov = prev_pfam_item[7] + pfam_item[7]
                    sign="---"
                else :
                    target_cov = 0
                
                if target_cov >= 0.7 and i_evalue1 <= 1 and i_evalue2 <= 1:
                    gid_dict[gid][pfam_id].remove(prev_pfam_item)
                    gid_dict[gid][pfam_id].remove(pfam_item)
                    if proper_continous :
                        coverage_list.append([env_start1,env_end2])
                        pfamda_txt +=  "%s%s %s %s %s %s %s %s %.2f %s %s\n"%(sign,gid,pfam_item[0],pfam_item[1],env_start1,env_end2,hmm_start1,hmm_end2,target_cov,pfam_item[8],pfam_item[9] )
                        pfam_id_list.append([pfam_item[0],pfam_item[1],pfam_item[3],pfam_item[4],pfam_item[8],pfam_item[9]])
                    else:
                        coverage_list.append([prev_pfam_item[3],prev_pfam_item[4]])
                        coverage_list.append([pfam_item[3],pfam_item[4]])
                        pfamda_txt += "%s%s %s %s %s %s %s %s %s %.2f %s %s\n"%(sign,gid,prev_pfam_item[0],prev_pfam_item[1],prev_pfam_item[2],prev_pfam_item[3],prev_pfam_item[4],prev_pfam_item[5],prev_pfam_item[6],prev_pfam_item[7],prev_pfam_item[8],prev_pfam_item[9] )
                        pfamda_txt += "%s%s %s %s %s %s %s %s %s %.2f %s %s\n"%(sign,gid,pfam_item[0],pfam_item[1],pfam_item[2],pfam_item[3],pfam_item[4],pfam_item[5],pfam_item[6],pfam_item[7],pfam_item[8],pfam_item[9] )
                        pfam_id_list.append([prev_pfam_item[0],prev_pfam_item[1],prev_pfam_item[3],prev_pfam_item[4],pfam_item[8],pfam_item[9]])
                        pfam_id_list.append([pfam_item[0],pfam_item[1],pfam_item[3],pfam_item[4],pfam_item[8],pfam_item[9]])                        
                    stretch_found = True
                else :
                    prev_pfam_item = pfam_item

        start_id = 0
        uncovered_region_list = []
        for covered_region in sorted(coverage_list, key=itemgetter(0)) :
            end_id = covered_region[0] - 1
            if (start_id < end_id) :
                uncovered_region_list.append([start_id,end_id])
            start_id = covered_region[1] + 1

        uncovered_region_list.append([start_id,100000])
        for pfam_id in gid_dict[gid] :
            for pfam_item in gid_dict[gid][pfam_id] :
                for uncovered_region in uncovered_region_list :
                    if (uncovered_region[0] - 26 < pfam_item[3] < uncovered_region[1] 
                    and uncovered_region[0] < pfam_item[4] < uncovered_region[1] + 26
                    and uncovered_region[1] - uncovered_region[0] > 35) :
                        if pfam_item[6] >= 0.7 and pfam_item[8] <= 1 :
                            uncovered_region_list.remove(uncovered_region)
                            uncovered_region_list.append([uncovered_region[0],pfam_item[3]])
                            if (uncovered_region[1] > pfam_item[4]) :
                                uncovered_region_list.append([pfam_item[4],uncovered_region[1]])
                        break
                else :
                        continue
                        
                if pfam_item[7] >= 0.7 and pfam_item[9] <= 1 :
                    pfamda_txt += "%s %s %s %s %s %s %s %s %.2f %s %s\n"%(gid,pfam_item[0],pfam_item[1],pfam_item[2],pfam_item[3],pfam_item[4],pfam_item[5],pfam_item[6],pfam_item[7],pfam_item[8],pfam_item[9] )
                    pfam_id_list.append([pfam_item[0],pfam_item[1],pfam_item[3],pfam_item[4],pfam_item[8],pfam_item[9]])
                    gid_dict[gid][pfam_id].remove(pfam_item)
                    #print pfam_id_list               
        if pfamda_txt != "" :
            out_fd.write(pfamda_txt)
        
        pfam_id_list = sorted(pfam_id_list, key=itemgetter(2))
        #print pfam_id_list
        pfam_id_str = ""
        pfam_desc_str = ""
        sf_id_str = ""
        env_cord_str = ""
        prev_start = 0
        prev_end = 0
        prev_ivalue = 1
        pfam_no_overlap_list = []
        prev_pfam_item = []
        for pfam_item in pfam_id_list :
            cur_start = pfam_item[2]
            cur_end = pfam_item[3]
            cur_ivalue = pfam_item[5]
            if ((cur_end  <= prev_end) or (cur_start  + 25 < prev_end )) :
                if (cur_ivalue < prev_ivalue) :
                    pfam_no_overlap_list.remove(prev_pfam_item)
                    pfam_no_overlap_list.append(pfam_item)
                else :
                    continue               
            else :
                pfam_no_overlap_list.append(pfam_item)
            
            prev_pfam_item = pfam_item
            prev_start = cur_start
            prev_end = cur_end
            prev_ivalue = cur_ivalue
                        
        for pfam_item in pfam_no_overlap_list :
            pfam_id_str += pfam_item[0] + "~"
            pfam_desc_str += pfam_item[1] +"~"
            env_cord_str += "%s-%s~"%(pfam_item[2],pfam_item[3])
            qlen_gid = pfam_item[4]
        if pfam_id_str != "" :
            da_fd.write("%s\t%s\t%s\t%s\t%s\n"%(gid,pfam_id_str[:-1],pfam_desc_str[:-1],env_cord_str[:-1],qlen_gid))        
            domain_arch = pfam_id_str[:-1]
            if domain_arch in domain_arch_dict :
                domain_arch_dict[domain_arch] += 1
            else :
                domain_arch_dict[domain_arch] = 1
                
    for domain_arch in domain_arch_dict :
        uf.write("%s %s\n" %(domain_arch,domain_arch_dict[domain_arch]))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="A tool to extract unique domain architecture")
    parser.add_argument('-i', dest="hmmout",required = True,help="Input HMM SCAN out")
    #parser.add_argument('-g', dest="gidfile",required = True,help="GID file")
    parser.add_argument('-p', dest="pfamda",default="pfamda_out.txt",help="Output PFAM DA file")
    parser.add_argument('-d', dest="domain",default="da_out.txt",help="Output DA file")
    parser.add_argument('-u', dest="uniqueDA",default="unique_da_out.txt",help="Output unique DA file")
    args_ = parser.parse_args()
    main(  )
    print( '[INFO] All done' )