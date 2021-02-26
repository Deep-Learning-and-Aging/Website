import pandas as pd
ETHNICITY_COLS = ['Do_not_know', 'Prefer_not_to_answer', 'NA', 'White', 'British',
       'Irish', 'White_Other', 'Mixed', 'White_and_Black_Caribbean',
       'White_and_Black_African', 'White_and_Asian', 'Mixed_Other', 'Asian',
       'Indian', 'Pakistani', 'Bangladeshi', 'Asian_Other', 'Black',
       'Caribbean', 'African', 'Black_Other', 'Chinese', 'Other_ethnicity',
       'Other']



x_dataset = ['Alcohol','Diet','Education','ElectronicDevices','Eyesight','Mouth','GeneralHealth','Breathing','Claudification','GeneralPain','ChestPain','CancerScreening','Medication','Hearing','Household','MentalHealth','OtherSociodemographics','PhysicalActivityQuestionnaire','SexualFactors','Sleep','Employment','FamilyHistory','SocialSupport','SunExposure','EarlyLifeFactors','Smoking']
medical = ['medical_diagnoses_%s' % letter for letter in ['A', 'B', 'C', 'D', 'E',
                                                    'F', 'G', 'H', 'I', 'J',
                                                    'K', 'L', 'M', 'N', 'O',
                                                    'P', 'Q', 'R', 'S', 'T',
                                                    'U', 'V', 'W', 'X', 'Y', 'Z']]

final_df = pd.DataFrame(columns = ['ID', 'Feature', 'Sub Field', 'Sample  Size', 'Number of Predictors'])
for elem in medical:
    print(elem)
    cols = pd.read_csv('/n/groups/patel/samuel/EWAS/inputs_final/%s.csv' % elem)
    cols_to_use = [elem for elem in cols.columns if elem not in ['Age', 'Age when attended assessment centre', 'Sex', 'eid', 'id'] + ETHNICITY_COLS +  ['Ethnicity.' + elem for elem in ETHNICITY_COLS] + ['ETHNICITY']]
    for column in cols_to_use:

        old_col = column
        column = column.replace('..', '.').replace('.0', '')
        splitted = column.split('.')
        if len(splitted) > 1 :
            feat_name = splitted[0]
            other_col = splitted[1]
            final_df = final_df.append({'ID' : elem, 'Feature' : feat_name, 'Sub Field' : other_col, 'Sample Size' : len(cols[old_col].dropna())}, ignore_index = True)
        else:
            feat_name = splitted[0]
            other_col = '-'
            final_df = final_df.append({'ID' : elem,  'Feature' : feat_name, 'Sub Field' : other_col, 'Sample Size' : len(cols[old_col].dropna())}, ignore_index = True)
final_df.to_csv('Summary_medical.csv')
