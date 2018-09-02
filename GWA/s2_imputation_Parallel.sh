## This script runs a genotype imputation pipeline.
## The pipeline is modelled after van Leeuwan 2015 (Nat Protocols)

## Routine I/O setup:
CUR_DIR=`pwd`
BASE_DIR="$(dirname $CUR_DIR)"
mkdir -p Jobs Logs Results
JOB_DIR=$CUR_DIR/Jobs
LOG_DIR=$CUR_DIR/Logs
OUT_DIR=$CUR_DIR/Results

## Set Dirs
DATA_DIR="/data/scratch/vlaufer/MEGA_AND_5M/Imputation/Data_to_be_Imputed/CLEAR_RADAR_5M"
DATA_FILE="CLEAR_RADAR_Omni_5M_RA_reorder.clean"
REF_DIR="/data/scratch/vlaufer/MEGA_AND_5M/Imputation/Ref_1kG_Phase3"

######################### Strand flip and prephasing with SHAPEIT2 ################################
echo "Now starting phasing with SHAPEIT2"
SHAPEIT="/data/scratch/vlaufer/MEGA_AND_5M/Imputation/ShapeIt/Static/bin/shapeit"
IMPUTE_DATA_DIR="/data/scratch/vlaufer/MEGA_AND_5M/Imputation/Ref_1kG_Phase3/1000GP_Phase3"
VCF_DATA_DIR="/data/scratch/vlaufer/MEGA_AND_5M/Imputation"
SUFFIX="phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz"
IMPUTE2="/data/scratch/vlaufer/MEGA_AND_5M/Imputation/IMPUTE2/impute_v2.3.2_x86_64_static/impute2"


# begin main loop to impute each chr:
for chr in {14..14}; do

	# Assign Vars
	STUDY_NAME="Imputation_FIVEM_chr${chr}"  #### Specify the name of your study. Should begin with letter, not number.
       	JOB_FILE=${JOB_DIR}/${STUDY_NAME}.sh
        LOG_FILE=${LOG_DIR}/${STUDY_NAME}
       	DATE=$(date)
        TARG_DIR=$DATA_DIR/chr${chr}
       	mkdir -p ${DATA_DIR}/chr${chr}/
        TARG_FILE=$DATA_DIR/chr${chr}/$DATA_FILE
       	namefile=${TARG_FILE}.HG19.for-impute.plink.chr${chr}.phased


        	cat > $JOB_FILE <<EOF
#!/bin/bash
# auto-generated job file
# generated from $PWD/$0
# on ${DATE}
#SBATCH --job-name=IMPUTE_FIVEM
#SBATCH --ntasks=1                              # Number of PROCESSES
#SBATCH --mem-per-cpu=32000                      # Memory specified for each core used (in MB) (no cores, use --mem=)
#SBATCH -t 5-00:00:00                           # Runtime in D-HH:MM:SS
#SBATCH --share
#SBATCH --partition=long                      # express(2h), short(12h), medium(2d2h), long(6d6h), interactive(2h)
#
#SBATCH --mail-user=${USER}@uab.edu
#SBATCH --mail-type=ALL                         # BEGIN, END, ERROR, ALL
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

	#Impute
# get the chunk widths going:
maxPos=\$(gawk '\$1!="position" {print \$1}' $IMPUTE_DATA_DIR/genetic_map_chr${chr}_combined_b37.txt | sort -n | tail -n 1)
nrChunk=\$(expr \${maxPos} "/" 5000000)
nrChunk2=\$(expr \${nrChunk} "+" 1)
start="0"

if [ ! -f ${namefile}.chunk\${chunk}.impute2 ]; then
	for chunk in \$(seq 1 \$nrChunk2); do # iterate over chunks

		endchr=\$(expr \$start "+" 5000000)
		startchr=\$(expr \$start "+" 1)
		$IMPUTE2 -known_haps_g ${namefile}.haps \
-m $IMPUTE_DATA_DIR/genetic_map_chr${chr}_combined_b37.txt \
-h $IMPUTE_DATA_DIR/1000GP_Phase3_chr${chr}.hap.gz \
-l $IMPUTE_DATA_DIR/1000GP_Phase3_chr${chr}.legend.gz \
-int \${startchr} \${endchr} -Ne 20000 -o ${namefile}.chunk\${chunk}.impute2
	start=\${endchr};
	done
fi
###########################
## End of your code here ##
###########################

srun hostname
srun sleep 15

EOF
                chmod 770 $JOB_FILE
                echo sbatch --mail-user=${USER}@uab.edu --job-name=${STUDY_NAME}_JOB $JOB_FILE
                sbatch --mail-user=${USER}@uab.edu --job-name=${STUDY_NAME}_JOB $JOB_FILE

done
