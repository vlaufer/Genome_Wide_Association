########################################################################
######## The purpose of this script is to output a standardized	########
######## 7 col. file so that processing by the PAINTOR utility  ########
######## scripts can begin.				  	########
########################################################################

## N.B. - Because this script takes raw input from potentially any study, it requires certain columns and for them to be named in a certain way.
## Specifically, the input file should have a header with the following fields (case sensitive; in any order): 
## RSID	Chr	Pos	EFFECT_ALLELE	ALT_ALLELE	Beta	SE	AF_cntl_Eff_Allele

##### Import any packages
import math
import sys
import itertools
import os

##### Do File and Folder processing 
i=0
input_file_array=[]
output_file_array=[]
ethnicity_array=[]
for study in sys.argv:
        if i==0:
                pass
        elif i==1:
                input_dir=sys.argv[i]
                print("the input directory is " + input_dir)
	elif i==2:
		input_array=sys.argv[i].split(',')
		for element in input_array:
			input_file_array.append(element + '.txt')
			output_file_array.append(element + "_proc.txt")
	elif i==3:
		ethnicity_array=sys.argv[i].split(',')	
        i+=1

print("the input files reformat are: " + " ".join(input_file_array) + "\n" + "the output files will be called: " + " ".join(output_file_array))
output_dir=input_dir + "proc/"
print("done setting file names and dirs")


##### Now process each file, output a file in standardized format for processing in the pipeline
for input_file,ethnicity,output_file in itertools.izip(input_file_array,ethnicity_array,output_file_array):
	data_dict={}
	### Do not run script if file already exists
	if os.path.isfile(output_dir + output_file) is True:
		print("The output files already exist. Moving to Pipeline Step 1")
		exit()
	else:
		pass

	with open(output_dir + output_file, 'a') as current_output_file:
		with open(input_dir + input_file, 'r') as current_input_file:
# Get column assignments
			header=current_input_file.readline()
			j=0
			header_line=header.strip().split()
	                for field in header_line:
        	                if field=="RSID":
					RSID_index=j
                	        if field=="Chr":
					Chr_index=j					
                        	if field=="Pos":
					Pos_index=j					
	                        if field=="EFFECT_ALLELE":
					Eff_Allele_index=j					
        	                if field=="ALT_ALLELE":
					Alt_Allele_index=j					
	                        if field=="Beta":
					Beta_index=j					
        	                if field=="SE":
					SE_index=j					
        	                if field=="AF_cntl_Eff_Allele":
					AF_cntl_Eff_Allele_index=j					
				j+=1

			current_output_file.write("RSID" + "\t" + "Chr" + "\t" + "Pos" + "\t" + "EFFECT_ALLELE" + "\t" + "ALT_ALLELE" + "\t" + "Z." + ethnicity + "\t" + "AF." + ethnicity + "\n")
			for line in current_input_file:
				out_line=[None]*7
				out_line[1]=""
				line=line.strip()
				line=line.split()
				out_line[0]=line[RSID_index]
				out_line[1]=line[Chr_index]
				out_line[2]=line[Pos_index]
				out_line[3]=line[Eff_Allele_index]
				out_line[4]=line[Alt_Allele_index]
				out_line[5]=str(float(line[Beta_index])/float(line[SE_index]))
				out_line[6]=line[AF_cntl_Eff_Allele_index]
				current_output_file.write("\t".join(out_line) + "\n")
		print("Created " + output_dir + output_file)

##### For Reference - Input file formats (use this to help with coding below)
#sys.argv[2] - "MegaGWAS_summary_Asian_chrpos.txt"
#RSID	NumericID	NeighGene	A1	A2	Num_Studies	Num_Cases	Num_Controls	AF_case_A1	AF_cntl_A1	Beta_A1	SE_A1	Pval_A1	Chr	Pos
#chr1:751343	100000751343	--	A	T	4	2843.0	5540.0	0.12726	0.14299	-0.16003	0.0625	0.010444025263187773	1	751343
#sys.argv[3] - "MegaGWAS_summary_European_chrpos.txt"
#RSID	NumericID	NeighGene	A1	A2	Num_Studies	Num_Cases	Num_Controls	AF_case_A1	AF_cntl_A1	Beta_A1	SE_A1	Pval_A1	Chr	Pos
#chr1:751343	100000751343	--	A	T	4	2843.0	5540.0	0.12726	0.14299	-0.16003	0.0625	0.010444025263187773	1	751343
#sys.argv[4] - "RA_GWASmeta_AA_v2_with_Z.txt"
#RSID	Chr	Pos	A1	A2	AF_cntl_A1	Pval_A1	OR_A1	ORL_A1	ORU_A1	Beta_A1	SE_A1	Z_A1
#rs6680825	1	91472	G	A	0.0472807	0.376351	0.516557	0.383828	0.695183	-0.165061	0.186586	-0.884637646983
