for CATEGORY in "ECGAtRest" "Employment" "Eyesight" "FamilyHistory" "Household" "Medication" "MentalHealth" "Mouth" "PhysicalActivity" "SocialSupport" "medical_diagnoses_B"
do
    for DIMENSION in "instances01" "instances1.5x" "instances23"
    do 
        aws s3 mv s3://age-prediction-site/page5_LinearXWASResults/LinearOutput/linear_correlations_$CATEGORY\__$DIMENSION.csv s3://age-prediction-site/page5_LinearXWASResults/LinearOutput/linear_correlations_$CATEGORY\_*$DIMENSION.csv
    done 
done