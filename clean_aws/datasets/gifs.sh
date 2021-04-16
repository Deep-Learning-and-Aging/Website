for CHAMBER_TYPE in "3_chambers" "4_chambers"
do
    for SEX in "female" "male"
    do
        for AGE_RANGE in "young" "middle" "old"
        do
            for GIF_PATH in data/datasets/videos/$CHAMBER_TYPE/$SEX/$AGE_RANGE/*
            do
                END_PATH=$(echo -n $GIF_PATH | tail -c 5)
                mv $GIF_PATH data/datasets/videos/$CHAMBER_TYPE/$SEX/$AGE_RANGE/sample_$END_PATH
            done
        done    
    done
done