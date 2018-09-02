# This script is a shell. It encodes a list of items (e.g. input file names) and runs them through the SLURM scheduler.
# It requires as input a text file containing each item. The script will then iterate over each item, submitting them to SLURM. SLURM handles the scheduling.
# The SBATCH commands below can be modified to the task at hand.

# Lines with One # are just notes.
# Lines with Four #### need to be modified each time
# Written by Vincent Laufer (brutuscassius@gmail.com) licensed under MIT license.
SNPTEST="/data/scratch/vlaufer/MEGA_AND_5M/Association_Testing/SNPTEST/snptest_v2.5.2_linux_x86_64_static/snptest_v2.5.2"

CUR_DIR=`pwd`
mkdir -p Jobs Logs Results
JOB_DIR=$CUR_DIR/Jobs
LOG_DIR=$CUR_DIR/Logs

ADIR="MS_sp"

## 1m1s
STUDY_NAME="Omni_1m1s_association_testing"                #### Specify the name of your study. Should begin with letter, not number.
DATA_DIR_MS="/data/scratch/vlaufer/Joint_Analysis/finalized_data_for_association_testing/MS"
SNPTEST="/data/scratch/vlaufer/MEGA_AND_5M/Association_Testing/SNPTEST/snptest_v2.5.2_linux_x86_64_static/snptest_v2.5.2"
OUT_DIR="/data/scratch/vlaufer/Joint_Analysis/Association_Results_Joint_Analysis/${ADIR}"
mkdir -p ${OUT_DIR} ${OUT_DIR}/merged

GEN_SUB_DIR="${CUR_DIR}/gen_split_filelists"
FILE_LIST="${GEN_SUB_DIR}/Omni1M_gen_subdivisions.txt"

# iterate and do work
while read FOLDER FILE_STEM block; do
        JOB_FILE=${JOB_DIR}/${STUDY_NAME}_${block}.sh
        LOG_FILE=${LOG_DIR}/${STUDY_NAME}_${block}
        DATE=$(date)

        cat > $JOB_FILE <<EOF
#!/bin/bash
# auto-generated job file
# generated from $PWD/$0
# on ${DATE}
#SBATCH --job-name=${chr}_JOB
#SBATCH --ntasks=1                          	# Number of PROCESSES
#SBATCH --mem-per-cpu=8000                  	# Memory specified for each core used (in MB) (no cores, use --mem=)
#SBATCH -t 2-02:00:00                       	# Runtime in D-HH:MM:SS
#SBATCH --share
#SBATCH --partition=medium                  	# express(2h), short(12h), medium(2d2h), long(6d6h), interactive(2h)
#
#SBATCH --mail-user=${USER}@uab.edu
#SBATCH --mail-type=ALL                     	# BEGIN, END, ERROR, ALL
#
#SBATCH --error=${LOG_FILE}.%j.%N.err.txt        # File to which STDERR will be written
#SBATCH --output=${LOG_FILE}.%j.%N.out.txt       # File to which STDOUT will be written
#
# Mimimum memory required per allocated  CPU  in  MegaBytes.
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=${USER}@uab.edu             #### Modify to your email address.
##

###########################
## Insert your code here ##
###########################

## with subjects excluded
# Additive model
/data/scratch/vlaufer/MEGA_AND_5M/Association_Testing/SNPTEST/snptest_v2.5.2_linux_x86_64_static/snptest_v2.5.2 -data  ${FOLDER}/${FILE_STEM}.block${block}.gen $DATA_DIR_MS/${FILE_STEM}.sample \
-o "${OUT_DIR}/${FILE_STEM}.block${block}.add" \
-frequentist 1 \
-method score \
-pheno plink_pheno \
-cov_names sex pc1 pc4 cohort \
-exclude_samples "${CUR_DIR}/exclusion_lists/Omni_1M1S_exclusion.seropos.list"


# Dominant model
/data/scratch/vlaufer/MEGA_AND_5M/Association_Testing/SNPTEST/snptest_v2.5.2_linux_x86_64_static/snptest_v2.5.2 -data  ${FOLDER}/${FILE_STEM}.block${block}.gen $DATA_DIR_MS/${FILE_STEM}.sample \
-o "${OUT_DIR}/${FILE_STEM}.block${block}.dom" \
-frequentist 2 \
-method score \
-pheno plink_pheno \
-cov_names sex pc1 pc4 cohort \
-exclude_samples "${CUR_DIR}/exclusion_lists/Omni_1M1S_exclusion.seropos.list"

srun hostname
srun sleep 15

EOF
		chmod 770 $JOB_FILE
		echo sbatch --mail-user=${USER}@uab.edu --job-name=${STUDY_NAME}_${chr}_JOB $JOB_FILE
		sbatch --mail-user=${USER}@uab.edu --job-name=${STUDY_NAME}_${chr}_JOB $JOB_FILE
done < "${FILE_LIST}"
