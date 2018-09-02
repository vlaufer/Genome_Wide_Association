import statistics; import sys

f1=sys.argv[1]
f2=sys.argv[2]
index=int(sys.argv[3])

# appearance of both files should be like this:
# 0	1		2	3	4	5	6	7	8	9		10		11		12
# chr	rsid		pos	a1	a2	aa	ab	bb	somemaf	somemaf		p		beta		se
# 1	rs12028261	714427	G	A	264.364	920.469	735.954	0.37724	0.402172	0.368157	-0.0558932	0.113052
# 1	rs11804379	715074	A	G	1725.86	187.563	7.499	0.052725	0.0511363	0.0533038	-0.394821	0.260013




def get_pvals(file, index_to_take):
	p_vector=[]
	with open(file, 'r') as f:
		for line in f:
			line=line.strip().split()
			p_vector.append(float(line[index_to_take]))
	return(p_vector)

def compare_p_vals(p_vector_1, p_vector_2):
	med1=statistics.median(p_vector_1)
	med2=statistics.median(p_vector_2)
	print("the median for the first study is " + str(med1) + " but the median for the second study is " + str(med2))


p1=get_pvals(f1, index)
p2=get_pvals(f2, index)
compare_p_vals(p1, p2)
