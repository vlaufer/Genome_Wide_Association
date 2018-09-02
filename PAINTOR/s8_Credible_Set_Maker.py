import sys
import os
import operator
from itertools import izip

i=0
file_stem_array=[]
locus_list=[]
eth_array=[]
Annotation_Bayes_Factors=""
for study in sys.argv:
	if i==1:
		result_file_dir=sys.argv[i]
	elif i==2:
		with open(sys.argv[i], 'r') as eth_file:
			for line in eth_file:
				line=line.strip().split()
				eth_array.append(line[0])
	elif i==3:
		anno_array=sys.argv[i].split(',')
	elif i==4:
		with open(sys.argv[i]) as out_dir_list:
			for line in out_dir_list:
				locus_list.append(line.strip())
	elif i==5:
		if os.path.isfile(sys.argv[i] + "/Annotation_Bayes_Factors.txt") is True:
			Annotation_Bayes_Factors=sys.argv[i] + "/Annotation_Bayes_Factors.txt"
		else:
			for file in os.listdir(sys.argv[i]):
				if file.startswith("Gname.Enrich"):
					gname_fh=sys.argv[i] + "/" + file
					with open(gname_fh, 'r') as infile:
						for line in infile:
							line=line.strip().split()
							if line[0]=="Baseline":
								pass
							else:
								Annotation_Bayes_Factors=sys.argv[i] + "/Annotation_Bayes_Factors.txt"
								with open(Annotation_Bayes_Factors, 'a') as ABF:
									ABF.write(line[0] + " " + line[1] + " " + gname_fh + "\n")
	elif i==6:
		annotation_dir=sys.argv[i]
        i+=1


## Make a dict linking Bayes Factors to Annotations
annotation_dict={}
with open(Annotation_Bayes_Factors, 'r') as enriched_annotations:
	for line in enriched_annotations:
		line=line.strip().split()
		annotation=line[2].split("/")
		annotation=annotation[-1]
		line[2]=annotation[13:]
		annotation_dict[line[2]]=line

## Make the credible sets:
curr_file=""
for eth in eth_array:
	for anno in anno_array:
		num_causal_array=anno.split("_")
		num_causal=num_causal_array[-1]
		curr_dir=result_file_dir + "/" + eth + "/" + anno
		for file in os.listdir(curr_dir):
			if file.endswith(".results"):
				curr_fh=curr_dir + "/" + file
				out_fh=curr_fh[:-8]
				print("working on " + out_fh + ".cred_set.txt ...")
				if os.path.isfile(out_fh + ".cred_set.txt") is True:
					print(out_fh + ".cred_set.txt" + " already exists. Skipping to next file")
					continue
				else:
					pass
				file_dict={}
				with open(curr_fh, 'r') as curr_file:
					header=curr_file.readline().strip()
					with open(out_fh + ".cred_set.txt", 'a') as out_file:
						out_file.write(header + " " + "Annotations" + "\n")
					for line in curr_file:
						line=line.strip().split()
						key=line[1] + ":" + line[2]
						file_dict[key]=float(line[8])
				sorted_file_dict = sorted(file_dict.items(), key=operator.itemgetter(1))
				num_snps_in_cc=0
				total_p_mass=0
				snps_in_cc=[]
				if num_causal=="1":
					p_threshold=0.9
				elif num_causal=="2":
					p_threshold=0.9
				while total_p_mass < p_threshold:
					num_snps_in_cc+=-1
					total_p_mass=total_p_mass + sorted_file_dict[num_snps_in_cc][-1]
					snps_in_cc.append(sorted_file_dict[num_snps_in_cc][0])

				for snp in snps_in_cc:
					file_array=file.split(".")
					file_stem=file_array[0]
					identifying_info=snp.split(":")
					annotation_file=annotation_dir + "/" + file_stem + ".annotations"
					annotation_file_row_number=1

# read from the .results and .annotation files at same time because they should have the same indexing.
					with open(curr_dir + "/" + file, 'r') as full_file, open(annotation_file, 'r') as enriched_annotations:
						full_file.readline()
						annot_header=enriched_annotations.readline().strip().split()
						file_row_number=1
						for full_line,annot_line in izip(full_file,enriched_annotations):
							full_line=full_line.strip().split()
							annot_line=annot_line.strip().split()
							if identifying_info[0] + identifying_info[1]==full_line[1] + full_line[2]:
								snp_annot_array=[]
								j=0
								for field in annot_line:
									if field == '1':
										if annot_header[j] in annotation_dict:
				                                                        if float(annotation_dict[annot_header[j]][1]) < -1:
												snp_annot_array.append(annotation_dict[annot_header[j]][2])
									j+=1
								with open(out_fh + ".cred_set.txt", 'a') as out_file:
									out_file.write(" ".join(full_line) + " " + ",".join(snp_annot_array) + "\n")
							else:
								pass
