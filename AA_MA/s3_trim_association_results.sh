# Omni_1M_1S_association_results.add.txt
model="add"
ms_analysis_dir="MS"
fm_analysis_dir="FM"
MS_DIR="/data/scratch/vlaufer/Joint_Analysis/Association_Results_Joint_Analysis/${ms_analysis_dir}/merged"
FM_DIR="/data/scratch/vlaufer/Joint_Analysis/Association_Results_Joint_Analysis/${fm_analysis_dir}/merged"
MS="${MS_DIR}/omni_1m_1s_chr_merged.trim.new_pc.recode.${model}"
FM="${FM_DIR}/imputed_qced_merged.5M.trim.new_pc.${model}"
MS_TRIM="${MS_DIR}/Omni_1M_1S_association_results.${model}.txt"
FM_TRIM="${FM_DIR}/Omni_5M_association_results.${model}.txt"

## additive model of inheritance
tail -n +13 $MS | awk '{print $1, $2, $4, $5, $6, $14, $15, $16, $29, $30, $31, $44, $45}' | grep -v "Completed" | awk '{gsub(/ /,"\t"); print $0}' > $MS_TRIM
tail -n +13 $FM | awk '{print $3, $2, $4, $5, $6, $14, $15, $16, $29, $30, $31, $44, $45}' | grep -v "Completed" | awk '{gsub(/ /,"\t"); print $0}' > $FM_TRIM

## dominant model of inheritance
model="dom"
MS_DIR="/data/scratch/vlaufer/Joint_Analysis/Association_Results_Joint_Analysis/${ms_analysis_dir}/merged"
FM_DIR="/data/scratch/vlaufer/Joint_Analysis/Association_Results_Joint_Analysis/${fm_analysis_dir}/merged"
MS="${MS_DIR}/omni_1m_1s_chr_merged.trim.new_pc.recode.${model}"
FM="${FM_DIR}/imputed_qced_merged.5M.trim.new_pc.${model}"
MS_TRIM="${MS_DIR}/Omni_1M_1S_association_results.${model}.txt"
FM_TRIM="${FM_DIR}/Omni_5M_association_results.${model}.txt"

tail -n +13 $MS | awk '{print $1, $2, $4, $5, $6, $14, $15, $16, $29, $30, $31, $44, $45}' | grep -v "Completed" | awk '{gsub(/ /,"\t"); print $0}' > $MS_TRIM
tail -n +13 $FM | awk '{print $3, $2, $4, $5, $6, $14, $15, $16, $29, $30, $31, $44, $45}' | grep -v "Completed" | awk '{gsub(/ /,"\t"); print $0}' > $FM_TRIM
