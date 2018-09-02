list_dir="./gen_split_filelists"

filelist=["Omni1M_assoc_files.txt", "Omni5M_assoc_files.txt"]

#omni_1m_1s_chr_merged.trim.new_pc.recode.add

for i in range(0, len(filelist)):
	with open(list_dir + "/" + filelist[i], 'r') as assoc_file_list:
		print(list_dir + "/" + filelist[i])
		k = 0
		for assoc_file in assoc_file_list:
			assoc_file=assoc_file.strip().split()
			assoc_file_name=assoc_file[0] + "/" + assoc_file[1] + ".block" + assoc_file[2] + ".add"
			print(assoc_file_name)
			with open(assoc_file[0] + "/merged" + "/" + assoc_file[1] + ".add", 'a') as out_file:
				with open(assoc_file_name, 'r') as results:
					j=0
					for line in results:
						if k == 0 and j > 12:
							out_file.write(line)
						elif j > 13:
							out_file.write(line)
						j+=1


			assoc_file_name=assoc_file[0] + "/" + assoc_file[1] + ".block" + assoc_file[2] + ".dom"
			with open(assoc_file[0] + "/merged" + "/" + assoc_file[1] + ".dom", 'a') as out_file2:
				with open(assoc_file_name, 'r') as results:
					j=0
					for line in results:
						if k == 0 and j > 12:
							out_file2.write(line)
						elif j > 13:
							out_file2.write(line)
						j+=1

