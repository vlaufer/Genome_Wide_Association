# This script is a shell. It encodes a list of items (e.g. input file names) and runs them through the SLURM scheduler.
# It requires as input a text file containing each item. The script will then iterate over each item, submitting them to SLURM. SLURM handles the scheduling.
# The SBATCH commands below can be modified to the task at hand.

# Lines with One # are just notes.
# Lines with Four #### need to be modified each time
# Written by Vincent Laufer (brutuscassius@gmail.com) licensed under MIT license.
module load PLINK/1.07-x86_64

CUR_DIR=`pwd`
BASE_DIR="$(dirname $CUR_DIR)"
mkdir -p Jobs Logs Results
JOB_DIR=$CUR_DIR/Jobs
LOG_DIR=$CUR_DIR/Logs
OUT_DIR=$CUR_DIR/Results

# For 5M
DATA_DIR="/data/scratch/vlaufer/MEGA_AND_5M/Imputation/Data_to_be_Imputed/CLEAR_RADAR_5M"
DATA_FILE="CLEAR_RADAR_Omni_5M_RA_reorder.clean"

######################### Strand flip and prephasing with SHAPEIT2 ################################
echo "Now starting phasing with SHAPEIT2"
SHAPEIT="/data/scratch/vlaufer/MEGA_AND_5M/Imputation/ShapeIt/Static/bin/shapeit"
IMPUTE_DATA_DIR="/data/scratch/vlaufer/MEGA_AND_5M/Imputation/Ref_1kG_Phase3/1000GP_Phase3"
VCF_DATA_DIR="/data/scratch/vlaufer/MEGA_AND_5M/Imputation"
SUFFIX="phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz"
IMPUTE2="/data/scratch/vlaufer/MEGA_AND_5M/Imputation/IMPUTE2/impute_v2.3.2_x86_64_static/impute2"
STUDY_NAME="FIVEM_Prephasing"                #### Specify the name of your study. Should begin with letter, not number.
STUDY_ID="CLEAR_RADAR_5M"
DATA_DIR="/data/scratch/vlaufer/MEGA_AND_5M/Imputation/Data_to_be_Imputed/$STUDY_ID"

# iterate and do work
for chr in {14..14}; do
        JOB_FILE=${JOB_DIR}/${STUDY_NAME}_${chr}.sh
        LOG_FILE=${LOG_DIR}/${STUDY_NAME}_${chr}
        DATE=$(date)
        TARG_DIR=$DATA_DIR/chr${chr}
        mkdir -p ${DATA_DIR}/chr${chr}/
        TARG_FILE=$DATA_DIR/chr${chr}/$DATA_FILE
        namefile=${TARG_FILE}.HG19.for-impute.plink.chr${chr}       	            ## MEGA

        cat > $JOB_FILE <<EOF
#!/bin/bash
# auto-generated job file
# generated from $PWD/$0
# on ${DATE}
#SBATCH --job-name=PREPHASE_${chr}_JOB
#SBATCH --ntasks=1                          	# Number of PROCESSES
#SBATCH --mem-per-cpu=8000                  	# Memory specified for each core used (in MB) (no cores, use --mem=)
#SBATCH -t 2-02:00:00                       	# Runtime in D-HH:MM:SS
#SBATCH --share
#SBATCH --partition=long                  	# express(2h), short(12h), medium(2d2h), long(6d6h), interactive(2h)
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
module load PLINK/1.07-x86_64

# initial shapeit run to detect flipped snps
        if [ ! -f ${namefile}.shapeit.flip.snp.strand ]; then
                $SHAPEIT -check \
--input-ped ${namefile}.nodup.ped ${namefile}.nodup.map \
--input-ref $IMPUTE_DATA_DIR/1000GP_Phase3_chr${chr}.hap.gz $IMPUTE_DATA_DIR/1000GP_Phase3_chr${chr}.legend.gz $IMPUTE_DATA_DIR/1000GP_Phase3.sample \
--output-log ${namefile}.shapeit.flip
        fi

# handle all the problem SNPs:
        if [ ! -f $TARG_DIR/duplicate_rsids_chr${chr}.txt ]; then
                awk '{print \$4}' ${namefile}.nodup.map | sort | uniq -c | awk '(\$1!=1){print \$0}' >> $TARG_DIR/duplicate_positions_in_chr${chr}.txt
		python get_rsid_for_dups_v2.py $chr "$TARG_DIR" $namefile
        fi

# exclude dups and flips
        if [ ! -f ${namefile}.proc.map ]; then
                grep "Missing" ${namefile}.shapeit.flip.snp.strand | awk '{print \$4}' > ${namefile}.to.exclude.txt
                cat $TARG_DIR/duplicate_rsids_chr${chr}.txt >> ${namefile}.to.exclude.txt
                grep "Strand" ${namefile}.shapeit.flip.snp.strand | awk '{print \$4}' > ${namefile}.to.flip.txt
                plink --file ${namefile}.nodup --flip ${namefile}.to.flip.txt --exclude ${namefile}.to.exclude.txt --recode --out ${namefile}.proc --noweb
        fi

## now rerun the alignment check.
        if [ ! -f ${namefile}.shapeit.proc2.snp.strand ]; then
                $SHAPEIT -check \
--input-ped ${namefile}.proc.ped ${namefile}.proc.map \
--input-ref  $IMPUTE_DATA_DIR/1000GP_Phase3_chr${chr}.hap.gz $IMPUTE_DATA_DIR/1000GP_Phase3_chr${chr}.legend.gz $IMPUTE_DATA_DIR/1000GP_Phase3.sample \
--output-log ${namefile}.proc2
        fi


	grep "Strand" ${namefile}.proc2.snp.strand | awk '{print \$4}' > ${namefile}.strand.flipped.snps2
## Create this list just to see if the new list is smaller (should be only snps that are mismatched, etc. now). safe to just exclude altogether.
## now should be able to exclude this smaller list and do the phasing:


        echo "#########################"
        echo "# do the actual phasing #"
        echo "#########################"

        if [ ! -f ${namefile}.phased.haps ]; then
        $SHAPEIT --input-ped ${namefile}.proc.ped ${namefile}.proc.map \
--exclude-snp ${namefile}.proc2.snp.strand.exclude \
--input-ref  $IMPUTE_DATA_DIR/1000GP_Phase3_chr${chr}.hap.gz $IMPUTE_DATA_DIR/1000GP_Phase3_chr${chr}.legend.gz $IMPUTE_DATA_DIR/1000GP_Phase3.sample \
--input-map $IMPUTE_DATA_DIR/genetic_map_chr${chr}_combined_b37.txt \
--output-max ${namefile}.phased \
--thread 8 \
--output-log ${namefile}.phased
        fi



###########################
## End of your code here ##
###########################

srun hostname
srun sleep 15

EOF
	chmod 770 $JOB_FILE
	echo sbatch --mail-user=${USER}@uab.edu --job-name=${STUDY_NAME}_${chr}_JOB $JOB_FILE
	sbatch --mail-user=${USER}@uab.edu --job-name=${STUDY_NAME}_${chr}_JOB $JOB_FILE
done
