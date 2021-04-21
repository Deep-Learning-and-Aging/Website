#!/bin/bash

DIMENSION="Arterial"
SUBDIMENSION="PulseWaveAnalysis"
for SUB_SUBDIMENSION in "TimeSeries"
do
    for SEX in "female" "male"
    do
        SEX_OLD=${SEX^}
        for AGE_GROUP in "young" "middle" "old"
        do
            for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
            do
                NEW_PATH=age-prediction-site/datasets/time_series/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX/$AGE_GROUP/sample_$SAMPLE.npy
                OLD_PATH=age-prediction-site/page15_AttentionMapsTimeSeries/img/Age/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_GROUP/normal/Saliency_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_GROUP\_normal\_$SAMPLE.npy

                aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
            done 
        done 
    done
done


DIMENSION="Heart"
SUBDIMENSION="ECG"
for SUB_SUBDIMENSION in "TimeSeries"
do
    for SEX in "female" "male"
    do
        SEX_OLD=${SEX^}
        for AGE_GROUP in "young" "middle" "old"
        do
            for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
            do
                NEW_PATH=age-prediction-site/datasets/time_series/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX/$AGE_GROUP/sample_$SAMPLE.npy
                OLD_PATH=age-prediction-site/page15_AttentionMapsTimeSeries/img/Age/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_GROUP/normal/Saliency_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_GROUP\_normal\_$SAMPLE.npy

                aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
            done 
        done 
    done
done


DIMENSION="PhysicalActivity"
SUBDIMENSION="FullWeek"
for SUB_SUBDIMENSION in "Acceleration"
do
    for SEX in "female" "male"
    do
        SEX_OLD=${SEX^}
        for AGE_GROUP in "young" "middle" "old"
        do
            for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
            do
                NEW_PATH=age-prediction-site/datasets/time_series/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX/$AGE_GROUP/sample_$SAMPLE.npy
                OLD_PATH=age-prediction-site/page15_AttentionMapsTimeSeries/img/Age/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_GROUP/normal/Saliency_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_GROUP\_normal\_$SAMPLE.npy

                aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
            done 
        done 
    done
done


DIMENSION="PhysicalActivity"
SUBDIMENSION="FullWeek"
for SUB_SUBDIMENSION in "TimeSeriesFeatures"
do
    for SEX in "female" "male"
    do
        SEX_OLD=${SEX^}
        for AGE_GROUP in "young" "middle" "old"
        do
            for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
            do
                NEW_PATH=age-prediction-site/datasets/time_series/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX/$AGE_GROUP/sample_$SAMPLE.npy
                OLD_PATH=age-prediction-site/page15_AttentionMapsTimeSeries/img/Age/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_GROUP/normal/Saliency_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_GROUP\_normal\_$SAMPLE.npy

                aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
            done 
        done 
    done
done


DIMENSION="PhysicalActivity"
SUBDIMENSION="Walking"
for SUB_SUBDIMENSION in "3D"
do
    for SEX in "female" "male"
    do
        SEX_OLD=${SEX^}
        for AGE_GROUP in "young" "middle" "old"
        do
            for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
            do
                NEW_PATH=age-prediction-site/datasets/time_series/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX/$AGE_GROUP/sample_$SAMPLE.npy
                OLD_PATH=age-prediction-site/page15_AttentionMapsTimeSeries/img/Age/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_GROUP/normal/Saliency_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_GROUP\_normal\_$SAMPLE.npy

                aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
            done 
        done 
    done
done

# if [ ! -f $OLD_PATH ]
# then
#     echo $OLD_PATH
# fi