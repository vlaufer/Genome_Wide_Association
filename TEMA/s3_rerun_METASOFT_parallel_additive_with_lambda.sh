# This script is a shell. It encodes a list of items (e.g. input file names) and runs them through the SLURM scheduler.
# It requires as input a text file containing each item. The script will then iterate over each item, submitting them to SLURM. SLURM handles the scheduling.
# The SBATCH commands below can be modified to the task at hand.

# Lines with One # are just notes.
# Lines with Four #### need to be modified each time
# Written by Vincent Laufer (brutuscassius@gmail.com) licensed under MIT license.

CUR_DIR=`pwd`
mkdir -p Jobs Logs Results
JOB_DIR=$CUR_DIR/Jobs
LOG_DIR=$CUR_DIR/Logs
OUT_DIR=$CUR_DIR/Results

#ANALYSIS_DIR="Joint_sex_pc1_pc4_cohort_v2"
ANALYSIS_DIR="Joint"
SPLIT_DIR="/data/scratch/vlaufer/Joint_Analysis/Association_Results_Joint_Analysis/${ANALYSIS_DIR}/split"
F_NAMES="${CUR_DIR}/reference_files/assoc_file_names_add.txt"

ls -1 ${SPLIT_DIR} | grep "additive" > temp.txt
awk '{gsub(/.in/,""); print $0}' temp.txt > ${F_NAMES}
rm temp.txt

# cat ${F_NAMES}
STUDY_NAME="METASOFT"                #### Specify the name of your study. Should begin with letter, not number.

# iterate and do work
while read MY_VAR; do
	FILE_PATH="${SPLIT_DIR}/${MY_VAR}"
        JOB_FILE=${JOB_DIR}/${STUDY_NAME}_${MY_VAR}.sh
        LOG_FILE=${LOG_DIR}/${STUDY_NAME}_${MY_VAR}
        DATE=$(date)

        cat > $JOB_FILE <<EOF
#!/bin/bash
# auto-generated job file
# generated from $PWD/$0
# on ${DATE}
#SBATCH --job-name=${STUDY_NAME}.${MY_VAR}_JOB
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

java -jar /data/scratch/vlaufer/OMNI_resubmission_analyses/validation/METASOFT/Metasoft.jar \
-input ${FILE_PATH}.in \
-output ${FILE_PATH}.with.lambda.seropos.out \
-mvalue -mvalue_p_thres 1E-6 \
-binary_effects -binary_effects_p_thres 1E-6 \
-lambda_mean 1.04555 \
-lambda_hetero 0.615819

###########################
## End of your code here ##
###########################

srun hostname
srun sleep 15

EOF

	chmod 770 $JOB_FILE
	echo sbatch --mail-user=${USER}@uab.edu --job-name=${STUDY_NAME}_${MY_VAR}_JOB $JOB_FILE
	sbatch --mail-user=${USER}@uab.edu --job-name=${STUDY_NAME}_${MY_VAR}_JOB $JOB_FILE

done < "${F_NAMES}"

