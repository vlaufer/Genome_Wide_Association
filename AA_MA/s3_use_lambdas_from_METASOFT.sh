
#  iterate and do work
FILE_PATH="/data/scratch/vlaufer/Joint_Analysis/Association_Results_Joint_Analysis/Joint/additive_association_results_for_METASOFT"
java -jar /data/scratch/vlaufer/OMNI_resubmission_analyses/validation/METASOFT/Metasoft.jar \
-input ${FILE_PATH}.in \
-output ${FILE_PATH}.with.lambda.noM.noBE.out \
-lambda_mean 1.04555 \
-lambda_hetero 0.615819 \
-log "./Logs/lambda_additive.log"

if [ 1 = 2  ]; then

	FILE_PATH="/data/scratch/vlaufer/Joint_Analysis/Association_Results_Joint_Analysis/Joint/dominant_association_results_for_METASOFT"
	java -jar /data/scratch/vlaufer/OMNI_resubmission_analyses/validation/METASOFT/Metasoft.jar \
-input ${FILE_PATH}.in \
-output ${FILE_PATH}.with.lambda.out \
-lambda_mean 1.04555 \
-lambda_hetero 0.615819 \
-log "./Logs/lambda_dominant.log"

fi
