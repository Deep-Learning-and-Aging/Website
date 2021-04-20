#!/bin/bash

DIMENSION="Abdomen"
SUBDIMENSION="Liver"
# mkdir all_data/datasets/images/$DIMENSION
# mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION
for SUB_SUBDIMENSION in "Contrast" "Raw"
do
    # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION
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
        # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY
        for SEX in "female" "male"
        do
            SEX_OLD=${SEX^}
            # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX
            for AGE_RANGE in "young" "middle" "old"
            do
                # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE
                for AGE_RATE in "accelerated" "normal" "decelerated"
                do 
                    # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE
                    for SAMPLE in "1" "2" "3" "4" "5" "6" "7" "8" "9"
                    do
                        NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
                        OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING
                        
                        aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
                    done 
                done 
            done
        done
    done
done


# DIMENSION="Abdomen"
# SUBDIMENSION="Pancreas"
# # mkdir all_data/datasets/images/$DIMENSION
# # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION
# for SUB_SUBDIMENSION in "Contrast" "Raw"
# do
#     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION
#     for DISPLAY in "Gradcam" "Raw" "Saliency"
#     do
#         if [ $DISPLAY == "Raw" ]
#         then
#             DISPLAY_OLD="RawImage"
#             ENDING="jpg"
#         else
#             DISPLAY_OLD=$DISPLAY
#             ENDING="npy"
#         fi
#         # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY
#         for SEX in "female" "male"
#         do
#             SEX_OLD=${SEX^}
#             # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX
#             for AGE_RANGE in "young" "middle" "old"
#             do
#                 # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE
#                 for AGE_RATE in "accelerated" "normal" "decelerated"
#                 do 
#                     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE
#                     for SAMPLE in "1" "2" "3" "4" "5" "6" "7" "8" "9"
#                     do
#                         NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
#                         OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING
                        
#                         aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
#                     done 
#                 done 
#             done
#         done
#     done
# done


# DIMENSION="Arterial"
# SUBDIMENSION="Carotids"
# # mkdir all_data/datasets/images/$DIMENSION
# # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION
# for SUB_SUBDIMENSION in "CIMT120" "CIMT150" "LongAxis" "Mixed" "ShortAxis"
# do
#     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION
#     for DISPLAY in "Gradcam" "Raw" "Saliency"
#     do
#         if [ $DISPLAY == "Raw" ]
#         then
#             DISPLAY_OLD="RawImage"
#             ENDING="jpg"
#         else
#             DISPLAY_OLD=$DISPLAY
#             ENDING="npy"
#         fi
#         # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY
#         for SEX in "female" "male"
#         do
#             SEX_OLD=${SEX^}
#             # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX
#             for AGE_RANGE in "young" "middle" "old"
#             do
#                 # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE
#                 for AGE_RATE in "accelerated" "normal" "decelerated"
#                 do 
#                     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE
#                     for SIDE in "left" "right"
#                     do
#                         for SAMPLE in "1" "2" "3" "4" "5" "6" "7" "8" "9"
#                         do
#                             NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/$SIDE\_sample_$SAMPLE.$ENDING
#                             OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$SIDE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE\_$SIDE.$ENDING
                            
#                             aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
#                         done 
#                     done
#                 done 
#             done
#         done
#     done
# done

# DIMENSION="Brain"
# SUBDIMENSION="MRI"
# # mkdir all_data/datasets/images/$DIMENSION
# # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION
# for SUB_SUBDIMENSION in "SagittalRaw" "SagittalReference" "CoronalRaw" "CoronalReference" "TransverseRaw" "TransverseReference"
# do
#     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION
#     for DISPLAY in "Gradcam" "Raw" "Saliency"
#     do
#         if [ $DISPLAY == "Raw" ]
#         then
#             DISPLAY_OLD="RawImage"
#             ENDING="jpg"
#         else
#             DISPLAY_OLD=$DISPLAY
#             ENDING="npy"
#         fi
#         # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY
#         for SEX in "female" "male"
#         do
#             SEX_OLD=${SEX^}
#             # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX
#             for AGE_RANGE in "young" "middle" "old"
#             do
#                 # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE
#                 for AGE_RATE in "accelerated" "normal" "decelerated"
#                 do 
#                     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE
#                     for SAMPLE in "1" "2" "3" "4" "5" "6" "7" "8" "9"
#                     do
#                         NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
#                         OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING

#                         aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
#                     done
#                 done 
#             done
#         done
#     done
# done


# DIMENSION="Eyes"
# SUBDIMENSION="Fundus"
# # mkdir all_data/datasets/images/$DIMENSION
# # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION
# for SUB_SUBDIMENSION in "Raw"
# do
#     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION
#     for DISPLAY in "Gradcam" "Raw" "Saliency"
#     do
#         if [ $DISPLAY == "Raw" ]
#         then
#             DISPLAY_OLD="RawImage"
#             ENDING="jpg"
#         else
#             DISPLAY_OLD=$DISPLAY
#             ENDING="npy"
#         fi
#         # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY
#         for SEX in "female" "male"
#         do
#             SEX_OLD=${SEX^}
#             # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX
#             for AGE_RANGE in "young" "middle" "old"
#             do
#                 # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE
#                 for AGE_RATE in "accelerated" "normal" "decelerated"
#                 do 
#                     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE
#                     for SIDE in "left" "right"
#                     do
#                         for SAMPLE in "1" "2" "3" "4" "5" "6" "7" "8" "9"
#                         do
#                             NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/$SIDE\_sample_$SAMPLE.$ENDING
#                             OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$SIDE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE\_$SIDE.$ENDING
                            
#                             aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
#                         done 
#                     done
#                 done 
#             done
#         done
#     done
# done

# DIMENSION="Eyes"
# SUBDIMENSION="OCT"
# # mkdir all_data/datasets/images/$DIMENSION
# # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION
# for SUB_SUBDIMENSION in "Raw"
# do
#     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION
#     for DISPLAY in "Gradcam" "Raw" "Saliency"
#     do
#         if [ $DISPLAY == "Raw" ]
#         then
#             DISPLAY_OLD="RawImage"
#             ENDING="jpg"
#         else
#             DISPLAY_OLD=$DISPLAY
#             ENDING="npy"
#         fi
#         # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY
#         for SEX in "female" "male"
#         do
#             SEX_OLD=${SEX^}
#             # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX
#             for AGE_RANGE in "young" "middle" "old"
#             do
#                 # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE
#                 for AGE_RATE in "accelerated" "normal" "decelerated"
#                 do 
#                     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE
#                     for SIDE in "left" "right"
#                     do
#                         for SAMPLE in "1" "2" "3" "4" "5" "6" "7" "8" "9"
#                         do
#                             NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/$SIDE\_sample_$SAMPLE.$ENDING
#                             OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$SIDE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE\_$SIDE.$ENDING
                            
#                             aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
#                         done 
#                     done
#                 done 
#             done
#         done
#     done
# done

# DIMENSION="Heart"
# SUBDIMENSION="MRI"
# # mkdir all_data/datasets/images/$DIMENSION
# # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION
# for SUB_SUBDIMENSION in "2chambersRaw" "2chambersContrast" "3chambersRaw" "3chambersContrast" "4chambersRaw" "4chambersContrast"
# do
#     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION
#     for DISPLAY in "Gradcam" "Raw" "Saliency"
#     do
#         if [ $DISPLAY == "Raw" ]
#         then
#             DISPLAY_OLD="RawImage"
#             ENDING="jpg"
#         else
#             DISPLAY_OLD=$DISPLAY
#             ENDING="npy"
#         fi
#         # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY
#         for SEX in "female" "male"
#         do
#             SEX_OLD=${SEX^}
#             # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX
#             for AGE_RANGE in "young" "middle" "old"
#             do
#                 # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE
#                 for AGE_RATE in "accelerated" "normal" "decelerated"
#                 do 
#                     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE
#                     for SAMPLE in "1" "2" "3" "4" "5" "6" "7" "8" "9"
#                     do
#                         NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
#                         OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING

#                         aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
#                     done
#                 done 
#             done
#         done
#     done
# done


# DIMENSION="Musculoskeletal"
# SUBDIMENSION="FullBody"
# # mkdir all_data/datasets/images/$DIMENSION
# # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION
# for SUB_SUBDIMENSION in "Figure" "Flesh" "Mixed" "Skeleton"
# do
#     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION
#     for DISPLAY in "Gradcam" "Raw" "Saliency"
#     do
#         if [ $DISPLAY == "Raw" ]
#         then
#             DISPLAY_OLD="RawImage"
#             ENDING="jpg"
#         else
#             DISPLAY_OLD=$DISPLAY
#             ENDING="npy"
#         fi
#         # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY
#         for SEX in "female" "male"
#         do
#             SEX_OLD=${SEX^}
#             # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX
#             for AGE_RANGE in "young" "middle" "old"
#             do
#                 # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE
#                 for AGE_RATE in "accelerated" "normal" "decelerated"
#                 do 
#                     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE
#                     for SAMPLE in "1" "2" "3" "4" "5" "6" "7" "8" "9"
#                     do
#                         NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
#                         OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING

#                         aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
#                     done
#                 done 
#             done
#         done
#     done
# done


# DIMENSION="Musculoskeletal"
# SUBDIMENSION="Knees"
# # mkdir all_data/datasets/images/$DIMENSION
# # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION
# for SUB_SUBDIMENSION in "DXA"
# do
#     SUB_SUBDIMENSION_OLD="MRI"
#     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION
#     for DISPLAY in "Gradcam" "Raw" "Saliency"
#     do
#         if [ $DISPLAY == "Raw" ]
#         then
#             DISPLAY_OLD="RawImage"
#             ENDING="jpg"
#         else
#             DISPLAY_OLD=$DISPLAY
#             ENDING="npy"
#         fi
#         # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY
#         for SEX in "female" "male"
#         do
#             SEX_OLD=${SEX^}
#             # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX
#             for AGE_RANGE in "young" "middle" "old"
#             do
#                 # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE
#                 for AGE_RATE in "accelerated" "normal" "decelerated"
#                 do 
#                     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE
#                     for SIDE in "left" "right"
#                     do
#                         for SAMPLE in "1" "2" "3" "4" "5" "6" "7" "8" "9"
#                         do
#                             NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/$SIDE\_sample_$SAMPLE.$ENDING
#                             OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION_OLD/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$SIDE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION_OLD\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE\_$SIDE.$ENDING

#                             aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
#                         done 
#                     done
#                 done 
#             done
#         done
#     done
# done


# DIMENSION="Musculoskeletal"
# SUBDIMENSION="Hips"
# # mkdir all_data/datasets/images/$DIMENSION
# # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION
# for SUB_SUBDIMENSION in "DXA"
# do
#     SUB_SUBDIMENSION_OLD="MRI"
#     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION
#     for DISPLAY in "Gradcam" "Raw" "Saliency"
#     do
#         if [ $DISPLAY == "Raw" ]
#         then
#             DISPLAY_OLD="RawImage"
#             ENDING="jpg"
#         else
#             DISPLAY_OLD=$DISPLAY
#             ENDING="npy"
#         fi
#         # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY
#         for SEX in "female" "male"
#         do
#             SEX_OLD=${SEX^}
#             # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX
#             for AGE_RANGE in "young" "middle" "old"
#             do
#                 # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE
#                 for AGE_RATE in "accelerated" "normal" "decelerated"
#                 do 
#                     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE
#                     for SIDE in "left" "right"
#                     do
#                         for SAMPLE in "1" "2" "3" "4" "5" "6" "7" "8" "9"
#                         do
#                             NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/$SIDE\_sample_$SAMPLE.$ENDING
#                             OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION_OLD/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$SIDE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION_OLD\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE\_$SIDE.$ENDING

#                             aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
#                         done 
#                     done
#                 done 
#             done
#         done
#     done
# done


# DIMENSION="Musculoskeletal"
# SUBDIMENSION="Spine"
# # mkdir all_data/datasets/images/$DIMENSION
# # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION
# for SUB_SUBDIMENSION in "Coronal" "Sagittal"
# do
#     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION
#     for DISPLAY in "Gradcam" "Raw" "Saliency"
#     do
#         if [ $DISPLAY == "Raw" ]
#         then
#             DISPLAY_OLD="RawImage"
#             ENDING="jpg"
#         else
#             DISPLAY_OLD=$DISPLAY
#             ENDING="npy"
#         fi
#         # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY
#         for SEX in "female" "male"
#         do
#             SEX_OLD=${SEX^}
#             # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX
#             for AGE_RANGE in "young" "middle" "old"
#             do
#                 # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE
#                 for AGE_RATE in "accelerated" "normal" "decelerated"
#                 do 
#                     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE
#                     for SAMPLE in "1" "2" "3" "4" "5" "6" "7" "8" "9"
#                     do
#                         NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
#                         OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING

#                         aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
#                     done
#                 done 
#             done
#         done
#     done
# done

# DIMENSION="PhysicalActivity"
# SUBDIMENSION="FullWeek"
# # mkdir all_data/datasets/images/$DIMENSION
# # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION
# for SUB_SUBDIMENSION in "GramianAngularField1minDifference" "GramianAngularField1minSummation" "MarkovTransitionField1min" "RecurrencePlots1min"
# do
#     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION
#     for DISPLAY in "Gradcam" "Raw" "Saliency"
#     do
#         if [ $DISPLAY == "Raw" ]
#         then
#             DISPLAY_OLD="RawImage"
#             ENDING="jpg"
#         else
#             DISPLAY_OLD=$DISPLAY
#             ENDING="npy"
#         fi
#         # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY
#         for SEX in "female" "male"
#         do
#             SEX_OLD=${SEX^}
#             # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX
#             for AGE_RANGE in "young" "middle" "old"
#             do
#                 # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE
#                 for AGE_RATE in "accelerated" "normal" "decelerated"
#                 do 
#                     # mkdir all_data/datasets/images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE
#                     for SAMPLE in "1" "2" "3" "4" "5" "6" "7" "8" "9"
#                     do
#                         NEW_PATH=age-prediction-site/datasets/images/$DIMENSION/$SUB_SUBDIMENSION/$DISPLAY/$SEX/$AGE_RANGE/$AGE_RATE/sample_$SAMPLE.$ENDING
#                         OLD_PATH=age-prediction-site/page9_AttentionMaps/Images/$DIMENSION/$SUBDIMENSION/$SUB_SUBDIMENSION/$SEX_OLD/$AGE_RANGE/$AGE_RATE/$DISPLAY_OLD\_Age_$DIMENSION\_$SUBDIMENSION\_$SUB_SUBDIMENSION\_$SEX_OLD\_$AGE_RANGE\_$AGE_RATE\_$SAMPLE.$ENDING

#                         aws s3 cp s3://$OLD_PATH s3://$NEW_PATH
#                     done
#                 done 
#             done
#         done
#     done
# done

# # if [ ! -f $OLD_PATH ]
# # then
# #     echo $OLD_PATH
# # fi