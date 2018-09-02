ms_analysis_dir="MS"
fm_analysis_dir="FM"
MS_DIR="/data/scratch/vlaufer/Joint_Analysis/Association_Results_Joint_Analysis/" + ms_analysis_dir + "/merged"
FM_DIR="/data/scratch/vlaufer/Joint_Analysis/Association_Results_Joint_Analysis/" + fm_analysis_dir + "/merged"

MS_TRIM=MS_DIR + "/Omni_1M_1S_association_results"
FM_TRIM=FM_DIR + "/Omni_5M_association_results"

file_array=[MS_TRIM, FM_TRIM]
model_array = ["add", "dom"]

for model in model_array:
	for file in file_array:
		infile=file + "." + model + ".txt"
		qc_in=file + "." + model + ".qc.in"
		qc_out=file + "." + model + ".qc.out"
		with open(qc_in, 'a') as in_file, open(qc_out, 'a') as out_file:
			with open(infile, 'r') as res_file:
				header=res_file.readline()
				header=header.strip().split()
				in_file.write("\t".join(header) + "\n")
				out_file.write("\t".join(header) + "\n")

				num_snps=0
				MAF_flags=0
				SE_flags=0
				ratio_flags=0
	
				for line in res_file:
					num_snps+=1
					line = line.strip().split()

					if len(line)!=13:
						continue
					if line[11] == "NA" or line[12] =="NA":
						continue			


					# make basic vars
					MAF=float(line[8])
					beta = float(line[11])
					SE = float(line[12])

					if SE > 0.6:
						SE_flags+=1
						out_file.write("\t".join(line) + "\n")
					elif MAF > 0.97 or MAF < 0.03:
						MAF_flags+=1
						out_file.write("\t".join(line) + "\n")
					else:
						in_file.write("\t".join(line) + "\n")
	
				print("total number of snps processed " + str(num_snps))
				print("total number of snps flagged based on standard error " + str(SE_flags))
				print("total number of snps flagged based on low MAF " + str(MAF_flags))

# new line numbering:
# 1 - chr
# 2 - snp
# 3 - pos
# 4 - a1
# 5 - a2
# 6 - AA
# 7 - AB
# 8 - BB
# 9 - MAF
# 10 - MAF
# 11 - MAF
# 12 - Beta
# 13 - SE
