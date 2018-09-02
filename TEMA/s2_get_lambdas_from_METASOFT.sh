
# iterate and do work
FILE_PATH="/data/scratch/vlaufer/Joint_Analysis/Association_Results_Joint_Analysis/Joint/dominant_association_results_for_METASOFT"
java -jar /data/scratch/vlaufer/OMNI_resubmission_analyses/validation/METASOFT/Metasoft.jar \
-input ${FILE_PATH}.in \
-output ${FILE_PATH}.getlambda.out \
-log "./Logs/lambda_dominant.log"


FILE_PATH="/data/scratch/vlaufer/Joint_Analysis/Association_Results_Joint_Analysis/Joint/additive_association_results_for_METASOFT"
java -jar /data/scratch/vlaufer/OMNI_resubmission_analyses/validation/METASOFT/Metasoft.jar \
-input ${FILE_PATH}.in \
-output ${FILE_PATH}.getlambda.out \
-log "./Logs/lambda_additive.log"
