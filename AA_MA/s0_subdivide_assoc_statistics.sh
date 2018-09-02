
# set files and folders
assoc_dir="/data/scratch/vlaufer/Joint_Analysis/finalized_data_for_association_testing"
MS_dir="${assoc_dir}/MS"
MS_gen_fh="${MS_dir}/omni_1m_1s_chr_merged.trim.new_pc.recode.gen"
MS_out_dir="${MS_dir}/gen_subdivisions"
MS_out_stem="${MS_out_dir}/omni_1m_1s_chr_merged.trim.new_pc.recode.block" 

FM_dir="${assoc_dir}/FM"
FM_gen_fh="${FM_dir}/imputed_qced_merged.5M.trim.new_pc.gen"
FM_out_dir="${FM_dir}/gen_subdivisions"
FM_out_stem="${FM_out_dir}/imputed_qced_merged.5M.trim.new_pc.block"

# split files

num_lines=40000

# 1m1s
split -l ${num_lines} -d ${MS_gen_fh} ${MS_out_stem}
for file in ${MS_out_stem}*; do
	mv "${file}" "${file}.txt"
done

# 5m
split -l ${num_lines} -d ${FM_gen_fh} ${FM_out_stem}
for file in ${FM_out_stem}*; do
	mv "${file}" "${file}.txt"
done
