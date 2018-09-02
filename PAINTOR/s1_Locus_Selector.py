import sys
import os

i=0
file_stem_array=[]
for study in sys.argv:
	if i==0:
		pass
	elif i==1:
		input_file_dir=sys.argv[i]
		print("the input directory is " + input_file_dir)
	elif i==2:
		ref_loci=sys.argv[i]
		print("the reference file containing the loci definitions is " + ref_loci)
	elif i==3:
		out_dir=sys.argv[i]
		print("the output directory is " + out_dir)
	elif i>3:
		input_array=study.split(',')
		for study in input_array:
			file_stem_array.append(study)
	i+=1

i=0
with open(ref_loci, 'r') as loci_for_extraction:
	for locus in loci_for_extraction:
		locus=locus.strip().split()
		print("currently working on " + " ".join(locus))
		for file_h in file_stem_array:
			with open(input_file_dir + file_h + "_proc.txt") as current_data_in:
				print("currently working on " + " ".join(locus) + " for " + file_h)
				header=current_data_in.readline()
#### Check to see if the output file already exists. If so, do not run.
				if os.path.isfile(out_dir + "/" + file_h + "_" + locus[0] + "_" + locus[1] + "_" + locus[2] + ".locus") is True:
					print(out_dir + "/" + file_h + "_" + locus[0] + "_" + locus[1] + "_" + locus[2] + ".locus already exists. Skipping to next file")
					continue
				else:
					pass
				with open(out_dir + "/" + file_h + "_" + locus[0] + "_" + locus[1] + "_" + locus[2] + ".locus", 'a') as out_file:
					out_file.write(header)
					for line in current_data_in:
						line=line.strip().split()
						try:
							if int(line[1])==int(locus[0]):
								if int(line[2]) >= int(locus[1]):
									if int(line[2]) <= int(locus[2]):						
										out_file.write(" ".join(line) + "\n")
						except ValueError:
							pass
# RSID	Chr	Pos	EFFECT_ALLELE	ALT_ALLELE	Z1	AF_cntl
# chr1:751343	1	751343	A	T	-2.56048	0.14299
