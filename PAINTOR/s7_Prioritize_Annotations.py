## This script takes the output from the individual tests of one annotation at a time.
## It then identifies the most enriched annotations, extracts them, and determines if they are uncorrelated.
## The uncorrelated ones can then be used in the final PAINTOR run.

#!/usr/bin/python

# Import modules
import sys
import glob
import collections
import pandas
import numpy
import csv


# name input args

#static
top_annot_number=50
r_threshold=0.5
#from user input
prep_dir=sys.argv[1]
temp_dir=sys.argv[2]
output_annot_file=sys.argv[3]
corr_mat=output_annot_file +  ".cormat.txt"

# make initial dict of all bayes factors and the annotation to which each corresponds 
BayesFactors=dict()
for filename in glob.glob( temp_dir + '/Gname*'):
	f_stem=filename.split("Gname.Enrich.")
	with open(filename, 'r') as file:
		for line in file:
			line=line.strip().split()
			print(line)
			if line[0]=='Baseline':
				pass
			else:
				BayesFactors[f_stem[1]] = float(line[1])
				print(float(line[1]))

# Get top 100 only, put in ordered dict
OrderedTopBF=collections.OrderedDict()
for key in sorted(BayesFactors, key=BayesFactors.get, reverse=False)[:top_annot_number]:
	OrderedTopBF[key] = BayesFactors[key]
# Make DataFrame with ALL annotations

all_annotation_files=glob.glob(prep_dir  + "/" + "*.annotations")
AnnotationsDF = pandas.concat((pandas.read_csv(f, sep=" ") for f in all_annotation_files))

# Restrict to columns containing top annotations
AnnotDFTrim=pandas.DataFrame()
for key in OrderedTopBF.keys():
	AnnotDFTrim[key]=AnnotationsDF[key]
print(AnnotDFTrim)

# Make correlation matrix for top annotations
correlation_matrix=numpy.corrcoef(AnnotDFTrim,rowvar=0)

# extract only desired annotations from the matrix
# Identify pairs of annotations with r2 greater than the r2 threshold
key_removal_list=[]
for i in range(0,top_annot_number):
	for j in range(0,top_annot_number):
		if i != j:
			print(correlation_matrix[i][j]*correlation_matrix[i][j])
			if correlation_matrix[i][j]*correlation_matrix[i][j] > r_threshold:
				if OrderedTopBF.items()[j][1] > OrderedTopBF.items()[i][1]:
					print("Need to remove " + OrderedTopBF.items()[i][0])
					key_removal_list.append(OrderedTopBF.items()[i][0])
key_removal_set=set(key_removal_list)

# remove all the keys corresponding to correlated annotations with low Bayes Factors
for key in key_removal_set:
	print(key)
	del AnnotDFTrim[key]

print(AnnotDFTrim)
correlation_matrix=numpy.corrcoef(AnnotDFTrim,rowvar=0)
print(correlation_matrix)

# write list of annotations
with open(output_annot_file, 'w') as annotations_to_keep:
	annotations_to_keep.write((",".join(AnnotDFTrim.columns.values)))

# Write correlation matrix to file, if desired
with open(corr_mat, 'w') as annotations_to_keep:
	cormat=numpy.ndarray.tolist(correlation_matrix)
	for line in cormat:
		line=[str(item) for item in line]
		annotations_to_keep.write(" ".join(line) + "\n")
