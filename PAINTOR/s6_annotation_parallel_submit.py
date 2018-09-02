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
STUDY_NAME="Locus_Annotation"                #### Specify the name of your study. Should begin with letter, not number.


####################################################################################################
#### Any Additional Variables you would like to declare (that are common to all jobs) go here.  ####
ANNOTATION_DIR="$1"
SCRIPT_DIR="$2"
ANNOTATION_BED_LIST="$3"
MERGE_DIR="$4"
REF_LOCI="$5"
BASE_DIR="$6"
####################################################################################################

# iterate and do work
while read CHR STARP ENDP; do
        LOCUS="chr"${CHR}_${STARP}_${ENDP}
        jobfile=${JOB_DIR}/${STUDY_NAME}_${LOCUS}.sh
        DATE=$(date)

        cat > $jobfile <<EOF
#!/bin/bash
# auto-generated job file
# generated from $PWD/$0
# on ${DATE}
#SBATCH --job-name=${VAR}_JOB
#SBATCH --ntasks=1                          	# Number of PROCESSES
#SBATCH --cpus-per-task=1                   	# Number of PROCESSES
#SBATCH --mem-per-cpu=3000                  	# Memory specified for each core used (in MB) (no cores, use --mem=)
#SBATCH -t 2-02:00:00                       	# Runtime in D-HH:MM:SS
#SBATCH --share
#SBATCH --partition=medium                  	# express(2h), short(12h), medium(2d2h), long(6d6h), interactive(2h)
#
#SBATCH --mail-user=${USER}@uab.edu
#SBATCH --mail-type=ALL                     	# BEGIN, END, ERROR, ALL
#
#SBATCH --error=${LOG_DIR}/${STUDY_NAME}_${LOCUS}.%j.%N.err.txt        # File to which STDERR will be written
#SBATCH --output=${LOG_DIR}/${STUDY_NAME}_${LOCUS}.%j.%N.out.txt       # File to which STDOUT will be written
#
# Mimimum memory required per allocated  CPU  in  MegaBytes.
#SBATCH --mem-per-cpu=8000
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=${USER}@uab.edu             #### Modify to your email address.
##

###########################
## Insert your code here ##
###########################

module load Python/2.7.9-goolf-1.7.20

if [ ! -f $ANNOTATION_DIR/${LOCUS}.annotations ]; then
	python $SCRIPT_DIR/Step_7_Annotate_Locus.py -i $ANNOTATION_BED_LIST -l $MERGE_DIR/${LOCUS} \
-o $ANNOTATION_DIR/${LOCUS}.annotations -c "Chr" -p "Pos" -d $BASE_DIR
else
	echo "Annotations file already exists at $ANNOTATION_DIR/${LOCUS}.annotations; skipping step."
fi


###########################
## End of your code here ##
###########################

srun hostname
srun sleep 30

EOF
		chmod 770 $jobfile
		echo sbatch --mail-user=${USER}@uab.edu --job-name=${STUDY_NAME}_${LOCUS}_JOB $jobfile
		sbatch --mail-user=${USER}@uab.edu --job-name=${STUDY_NAME}_${LOCUS}_JOB $jobfile
done < "$REF_LOCI"

