import glob; import os; import sys; import itertools
from collections import OrderedDict

input_dir=sys.argv[1]

loci_to_merge=[]
for file in glob.glob(input_dir + "/*"):
	f_array=file.split(".")
	
	loci_to_merge.append(f_array[0])

ltms=set(loci_to_merge)

i=0
for locus in ltms:

	i+=1
	print("now working on locus (the number " + str(i) + " file).")  
	eur_file = locus + ".EUR"; eas_file = locus + ".EAS"; afr_file = locus + ".AFR"; out_file=locus + ".merge"
	merge_dict=OrderedDict()

	if not os.path.isfile(eur_file):
		print(" no EUR file, skipping locus")
		continue
	elif not os.path.isfile(eas_file):
		print(" no EAS file, skipping locus")
		continue
	elif not os.path.isfile(afr_file): 
		print(" no AFR file, skipping locus")
		continue

	with open(eur_file, 'r') as eurf:
		header=eurf.readline()
		for line in eurf:
			line=line.strip().split()
			new_entry=line[1] + ":" + line[2]
			if new_entry in merge_dict:
				pass
			else:
				merge_dict[new_entry] = ["NA"] * 11
				merge_dict[new_entry][0:5] = line[0:5]
				merge_dict[new_entry][5] = line[5]
				merge_dict[new_entry][6] = line[6]

	with open(eas_file, 'r') as easf:
		header=easf.readline()
		for line in easf:
			line=line.strip().split()
			new_entry=line[1] + ":" + line[2]
			if new_entry in merge_dict:
				merge_dict[new_entry][7] = line[5]
				merge_dict[new_entry][8] = line[6]
				if line[3] != merge_dict[new_entry][3] or line[4] != merge_dict[new_entry][4]:
					print(merge_dict[new_entry], line)	# this is a qc measure - if anything is printed, means the alleles were not matched appropriately.
			else:
				merge_dict[new_entry] = ["NA"] * 11
				merge_dict[new_entry][0:5] = line[0:5]
				merge_dict[new_entry][7] = line[5]
				merge_dict[new_entry][8] = line[6]


	with open(afr_file, 'r') as afrf:
		header=afrf.readline()
		for line in afrf:
			line=line.strip().split()
			new_entry=line[1] + ":" + line[2]
			if new_entry in merge_dict:
				merge_dict[new_entry][9] = line[5]
				merge_dict[new_entry][10] = line[6]
				if line[3] != merge_dict[new_entry][3] or line[4] != merge_dict[new_entry][4]:
					print(merge_dict[new_entry], line)	# this is a qc measure - if anything is printed, means the alleles were not matched appropriately.
			else:
				merge_dict[new_entry] = ["NA"] * 11
				merge_dict[new_entry][0:5] = line[0:5]
				merge_dict[new_entry][9] = line[5]
				merge_dict[new_entry][10] = line[6]
	with open(out_file, 'a') as out_fh:
		for key, value in sorted(merge_dict.iteritems(), key = lambda e: (e[1][1])):
			out_fh.write(":".join(value[0:5]) + "\t" +"\t".join(value[5:]) + "\n")
