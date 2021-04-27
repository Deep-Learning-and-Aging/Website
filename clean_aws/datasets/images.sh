#!/bin/bash

DIMENSION="Abdomen"
SUBDIMENSION="Liver"
for SUB_SUBDIMENSION in "Contrast" "Raw"
do
    for DISPLAY in "Gradcam" "Raw" "Saliency"
    do
        if [ $DISPLAY == "Raw" ]
        then
            DISPLAY_OLD="RawImage"
            ENDING="jpg"
        else
            DISPLAY_OLD=$DISPLAY
            ENDING="npy"
        fi
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            for AGE_RANGE in "young" "middle" "old"
            do
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
                    do
                        NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
                        OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING
                        
                        aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                    done 
                done 
            done
        done
    done
done


DIMENSION="Abdomen"
SUBDIMENSION="Pancreas"
for SUB_SUBDIMENSION in "Contrast" "Raw"
do
    for DISPLAY in "Gradcam" "Raw" "Saliency"
    do
        if [ $DISPLAY == "Raw" ]
        then
            DISPLAY_OLD="RawImage"
            ENDING="jpg"
        else
            DISPLAY_OLD=$DISPLAY
            ENDING="npy"
        fi
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            for AGE_RANGE in "young" "middle" "old"
            do
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
                    do
                        NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
                        OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING
                        
                        aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                    done 
                done 
            done
        done
    done
done


DIMENSION="Arterial"
SUBDIMENSION="Carotids"
for SUB_SUBDIMENSION in "CIMT120" "CIMT150" "LongAxis" "Mixed" "ShortAxis"
do
    for DISPLAY in "Gradcam" "Raw" "Saliency"
    do
        if [ $DISPLAY == "Raw" ]
        then
            DISPLAY_OLD="RawImage"
            ENDING="jpg"
        else
            DISPLAY_OLD=$DISPLAY
            ENDING="npy"
        fi
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            for AGE_RANGE in "young" "middle" "old"
            do
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    for SIDE in "left" "right"
                    do
                        for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
                        do
                            NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/$SIDE\_sample_$SAMPLE.$ENDING
                            OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$SIDE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE\_$SIDE.$ENDING
                            
                            aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                        done 
                    done
                done 
            done
        done
    done
done

DIMENSION="Brain"
SUBDIMENSION="MRI"
for SUB_SUBDIMENSION in "SagittalRaw" "SagittalReference" "CoronalRaw" "CoronalReference" "TransverseRaw" "TransverseReference"
do
    for DISPLAY in "Gradcam" "Raw" "Saliency"
    do
        if [ $DISPLAY == "Raw" ]
        then
            DISPLAY_OLD="RawImage"
            ENDING="jpg"
        else
            DISPLAY_OLD=$DISPLAY
            ENDING="npy"
        fi
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            for AGE_RANGE in "young" "middle" "old"
            do
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
                    do
                        NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
                        OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING

                        aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                    done
                done 
            done
        done
    done
done


DIMENSION="Eyes"
SUBDIMENSION="Fundus"
for SUB_SUBDIMENSION in "Raw"
do
    for DISPLAY in "Gradcam" "Raw" "Saliency"
    do
        if [ $DISPLAY == "Raw" ]
        then
            DISPLAY_OLD="RawImage"
            ENDING="jpg"
        else
            DISPLAY_OLD=$DISPLAY
            ENDING="npy"
        fi
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            for AGE_RANGE in "young" "middle" "old"
            do
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    for SIDE in "left" "right"
                    do
                        for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
                        do
                            NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/$SIDE\_sample_$SAMPLE.$ENDING
                            OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$SIDE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE\_$SIDE.$ENDING
                            
                            aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                        done 
                    done
                done 
            done
        done
    done
done

DIMENSION="Eyes"
SUBDIMENSION="OCT"
for SUB_SUBDIMENSION in "Raw"
do
    for DISPLAY in "Gradcam" "Raw" "Saliency"
    do
        if [ $DISPLAY == "Raw" ]
        then
            DISPLAY_OLD="RawImage"
            ENDING="jpg"
        else
            DISPLAY_OLD=$DISPLAY
            ENDING="npy"
        fi
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            for AGE_RANGE in "young" "middle" "old"
            do
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    for SIDE in "left" "right"
                    do
                        for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
                        do
                            NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/$SIDE\_sample_$SAMPLE.$ENDING
                            OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$SIDE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE\_$SIDE.$ENDING
                            
                            aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                        done 
                    done
                done 
            done
        done
    done
done

DIMENSION="Heart"
SUBDIMENSION="MRI"
for SUB_SUBDIMENSION in "2chambersRaw" "2chambersContrast" "3chambersRaw" "3chambersContrast" "4chambersRaw" "4chambersContrast"
do
    for DISPLAY in "Gradcam" "Raw" "Saliency"
    do
        if [ $DISPLAY == "Raw" ]
        then
            DISPLAY_OLD="RawImage"
            ENDING="jpg"
        else
            DISPLAY_OLD=$DISPLAY
            ENDING="npy"
        fi
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            for AGE_RANGE in "young" "middle" "old"
            do
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
                    do
                        NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
                        OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING

                        aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                    done
                done 
            done
        done
    done
done


DIMENSION="Musculoskeletal"
SUBDIMENSION="FullBody"
for SUB_SUBDIMENSION in "Figure" "Flesh" "Mixed" "Skeleton"
do
    for DISPLAY in "Gradcam" "Raw" "Saliency"
    do
        if [ $DISPLAY == "Raw" ]
        then
            DISPLAY_OLD="RawImage"
            ENDING="jpg"
        else
            DISPLAY_OLD=$DISPLAY
            ENDING="npy"
        fi
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            for AGE_RANGE in "young" "middle" "old"
            do
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
                    do
                        NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
                        OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING

                        aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                    done
                done 
            done
        done
    done
done


DIMENSION="Musculoskeletal"
SUBDIMENSION="Knees"
for SUB_SUBDIMENSION in "DXA"
do
    SUB_SUBDIMENSION_OLD="MRI"
    for DISPLAY in "Gradcam" "Raw" "Saliency"
    do
        if [ $DISPLAY == "Raw" ]
        then
            DISPLAY_OLD="RawImage"
            ENDING="jpg"
        else
            DISPLAY_OLD=$DISPLAY
            ENDING="npy"
        fi
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            for AGE_RANGE in "young" "middle" "old"
            do
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    for SIDE in "left" "right"
                    do
                        for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
                        do
                            NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/$SIDE\_sample_$SAMPLE.$ENDING
                            OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION_OLD/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$SIDE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION_OLD\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE\_$SIDE.$ENDING

                            aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                        done 
                    done
                done 
            done
        done
    done
done


DIMENSION="Musculoskeletal"
SUBDIMENSION="Hips"
for SUB_SUBDIMENSION in "DXA"
do
    SUB_SUBDIMENSION_OLD="MRI"
    for DISPLAY in "Gradcam" "Raw" "Saliency"
    do
        if [ $DISPLAY == "Raw" ]
        then
            DISPLAY_OLD="RawImage"
            ENDING="jpg"
        else
            DISPLAY_OLD=$DISPLAY
            ENDING="npy"
        fi
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            for AGE_RANGE in "young" "middle" "old"
            do
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    for SIDE in "left" "right"
                    do
                        for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
                        do
                            NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/$SIDE\_sample_$SAMPLE.$ENDING
                            OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION_OLD/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$SIDE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION_OLD\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE\_$SIDE.$ENDING

                            aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                        done 
                    done
                done 
            done
        done
    done
done


DIMENSION="Musculoskeletal"
SUBDIMENSION="Spine"
for SUB_SUBDIMENSION in "Coronal" "Sagittal"
do
    for DISPLAY in "Gradcam" "Raw" "Saliency"
    do
        if [ $DISPLAY == "Raw" ]
        then
            DISPLAY_OLD="RawImage"
            ENDING="jpg"
        else
            DISPLAY_OLD=$DISPLAY
            ENDING="npy"
        fi
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            for AGE_RANGE in "young" "middle" "old"
            do
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
                    do
                        NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
                        OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING

                        aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                    done
                done 
            done
        done
    done
done

DIMENSION="PhysicalActivity"
SUBDIMENSION="FullWeek"
for SUB_SUBDIMENSION in "GramianAngularField1minDifference" "GramianAngularField1minSummation" "MarkovTransitionField1min" "RecurrencePlots1min"
do
    for DISPLAY in "Gradcam" "Raw" "Saliency"
    do
        if [ $DISPLAY == "Raw" ]
        then
            DISPLAY_OLD="RawImage"
            ENDING="jpg"
        else
            DISPLAY_OLD=$DISPLAY
            ENDING="npy"
        fi
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            for AGE_RANGE in "young" "middle" "old"
            do
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    for SAMPLE in "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
                    do
                        NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
                        OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING

                        aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                    done
                done 
            done
        done
    done
done

# # if [ ! -f $OLD_PATH ]
# # then
# #     echo $OLD_PATH
# # fi