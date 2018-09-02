## purpose of this script is to remove variants that are very unlikely to be informative in the fine-mapping process.
import os
import sys

output_dir=sys.argv[1]
input_dir=sys.argv[2]
file_stem=sys.argv[3]

input_file=input_dir + "/" + file_stem
out_file_name=output_dir + "/" + file_stem

print(input_file)
print(out_file_name)
if os.path.isfile(out_file_name) is True:
        print(input_file + " already exists. Skipping trim step for this locus. \n")
        exit()

with open(out_file_name, 'a') as out_file:
	with open(input_file, 'r') as locus:
		header=locus.readline()
		out_file.write(header)
		for line in locus:			## At this point, lines look like this:
			line=line.strip().split()    	## ['chr5:8004319', 'chr5', '8004319', 'T', 'C', 'NA', '-0.425757821365', 'NA']
			sumZ=0
			NA_count=0

			for i in range(5, len(line)):
				if line[i]=="NA":
					NA_count+=1
				else:
					sumZ=float(sumZ) + abs(float(line[i]))

			num_eth=len(line) - (5 + NA_count)		
			if num_eth==1 and float(sumZ) < 1.5:
				continue
#			elif (float(sumZ)/float(num_eth)) < 1:
#				continue
			else:
				out_file.write(" ".join(line) + "\n")

