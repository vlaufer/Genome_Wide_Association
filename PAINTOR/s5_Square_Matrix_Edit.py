import sys

file=sys.argv[1] + ".ld"

ofile=sys.argv[1] + ".LD"
with open(ofile, 'a') as out_file:
        with open(file, 'r') as infile:
                i=0
                for line in infile:
                        j=0
                        line=line.strip()
                        line=line.split()
                        for cell in line:
                                if cell=="nan":
                                        line[j]="0"
                                if i==j:
                                        line[j]="1.0000e+00"
                                j+=1
                        out_file.write(" ".join(line) + "\n")
                        i+=1
