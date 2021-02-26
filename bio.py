import numpy as np
import pandas as pd
import glob
import os
final_df = pd.DataFrame(columns = ['Main dimension', 'Subdimension', 'Sub-subdimension', 'Feature', 'Sub Field', 'Sample Size'])
list_models = ['Correlation', 'ElasticNet', 'LightGBM', 'NeuralNetwork']
ETHNICITY_COLS = ['Do_not_know', 'Prefer_not_to_answer', 'NA', 'White', 'British',
       'Irish', 'White_Other', 'Mixed', 'White_and_Black_Caribbean',
       'White_and_Black_African', 'White_and_Asian', 'Mixed_Other', 'Asian',
       'Indian', 'Pakistani', 'Bangladeshi', 'Asian_Other', 'Black',
       'Caribbean', 'African', 'Black_Other', 'Chinese', 'Other_ethnicity',
       'Other']



path_feat_imps = '/Users/samuel/Desktop/Dash-Website/data/page3_featureImp/FeatureImp/'
dict_dataset_images_to_organ_and_view = {
    'Brain' : {
        'MRI' : ['SagittalRaw', 'SagittalReference', 'CoronalRaw', 'CoronalReference', 'TransverseRaw', 'TransverseReference']
        },
    'Eyes' : {
        'Fundus' : ['Raw'],
        'OCT' : ['Raw']
        },
    'Arterial' : {
        'Carotids' : ['Mixed', 'LongAxis', 'CIMT120', 'CIMT150', 'ShortAxis']
        },
    'Heart' : {
        'MRI' : ['2chambersRaw', '2chambersContrast', '3chambersRaw', '3chambersContrast', '4chambersRaw', '4chambersContrast']
        },
    'Abdomen' : {
        'Liver' : ['Raw', 'Contrast'],
        'Pancreas' : ['Raw', 'Contrast']
        },
    'Musculoskeletal' : {
        'Spine' : ['Sagittal', 'Coronal'],
        'Hips' : ['MRI'],
        'Knees' : ['MRI'],
        'FullBody' : ['Mixed', 'Figure', 'Skeleton', 'Flesh']
        },
    'PhysicalActivity' : {
        'FullWeek': ['GramianAngularField1minDifference','GramianAngularField1minSummation', 'MarkovTransitionField1min', 'RecurrencePlots1min']
    }

}

dict_dataset_to_organ_and_view = {
    ## Brain
    'BrainGreyMatterVolumes' : ('Brain', 'MRI', 'GreyMatterVolumes'),
    'BrainSubcorticalVolumes': ('Brain', 'MRI', 'SubcorticalVolumes'),
    'BraindMRIWeightedMeans' : ('Brain', 'MRI', 'dMRIWeightedMeans'),
    'BrainMRIAllBiomarkers' : ('Brain', 'MRI', 'AllScalars'),
    'CognitiveReactionTime' : ('Brain', 'Cognitive', 'ReactionTime'),
    'CognitiveMatrixPatternCompletion' : ('Brain', 'Cognitive', 'MatrixPatternCompletion'),
    'CognitiveTowerRearranging' : ('Brain', 'Cognitive', 'TowerRearranging'),
    'CognitiveSymbolDigitSubstitution' : ('Brain', 'Cognitive', 'SymbolDigitSubstitution'),
    'CognitivePairedAssociativeLearning' : ('Brain', 'Cognitive', 'PairedAssociativeLearning'),
    'CognitiveProspectiveMemory' : ('Brain', 'Cognitive', 'ProspectiveMemory'),
    'CognitiveNumericMemory' : ('Brain', 'Cognitive', 'NumericMemory'),
    'CognitiveFluidIntelligence' : ('Brain', 'Cognitive', 'FluidIntelligence'),
    'CognitiveTrailMaking' : ('Brain', 'Cognitive', 'TrailMaking'),
    'CognitivePairsMatching' : ('Brain', 'Cognitive', 'PairsMatching'),
    'CognitiveAllBiomarkers' : ('Brain', 'Cognitive', 'AllScalars'),
    'BrainAndCognitive' : ('Brain', 'All', 'Scalars'),
    ## Eyes
    'EyeAutorefraction' : ('Eyes', 'Autorefraction', 'Scalars'),
    'EyeAcuity' : ('Eyes', 'Acuity', 'Scalars'),
    'EyeIntraocularPressure' : ('Eyes', 'IntraocularPressure', 'Scalars'),
    'EyesAllBiomarkers' : ('Eyes', 'All', 'Scalars'),
    # Hearing
    'HearingTest' : ('Hearing', 'HearingTest', 'Scalars'),
    # Lungs
    'Spirometry' :  ('Lungs', 'Spirometry', 'Scalars'),
    # Vascular
    'BloodPressure' : ('Arterial', 'BloodPressure', 'Scalars'),
    'CarotidUltrasound' : ('Arterial', 'Carotids', 'Scalars'),
    'ArterialStiffness' : ('Arterial', 'PWA', 'Scalars'),
    'VascularAllBiomarkers' : ('Arterial', 'All', 'Scalars'),
    # Heart
    'HeartAllBiomarkers' : ('Heart', 'All', 'Scalars'),
    'HeartSize' : ('Heart', 'MRI', 'Size'),
    'HeartPWA' : ('Heart', 'MRI', 'PWA'),
    'HeartMRIAll' : ('Heart', 'MRI', 'AllScalars'),
    'ECGAtRest' : ('Heart', 'ECG', 'Scalars'),

    # Musculoskeletal
    'AnthropometryImpedance' : ('Musculoskeletal', 'Scalars', 'Impedance'),
    'AnthropometryBodySize' : ('Musculoskeletal', 'Scalars', 'Anthropometry'),
    'BoneDensitometryOfHeel' : ('Musculoskeletal', 'Scalars', 'HeelBoneDensitometry'),
    'HandGripStrength' : ('Musculoskeletal', 'Scalars', 'HandGripStrength'),
    'MusculoskeletalAllBiomarkers' : ('Musculoskeletal', 'Scalars', 'AllScalars'),

    #Biochemistry
    'BloodBiochemistry' : ('Biochemistry', 'Blood', 'Scalars'),
    'UrineBiochemistry' : ('Biochemistry', 'Urine', 'Scalars'),
    'Biochemistry' : ('Biochemistry', 'All', 'Scalars'),
    #ImmuneSystem
    'BloodCount' : ('ImmuneSystem', 'BloodCount', 'Scalars'),  # Need to do blood infection
    'PhysicalActivity' : ('PhysicalActivity', 'FullWeek', 'Scalars')
}

path_score_scalar = '/Users/samuel/Desktop/Dash-Website/data/page2_predictions/Performances/PERFORMANCES_tuned_alphabetical_eids_Age_test.csv'
score = pd.read_csv(path_score_scalar)
dict_organ_view_transf_to_id = { v : k for k, v in dict_dataset_to_organ_and_view.items()}

hierarchy_biomarkers = dict()
for key1, key2, value in dict_dataset_to_organ_and_view.values():
    if key1 not in hierarchy_biomarkers.keys():
        hierarchy_biomarkers[key1] = {}
    if key2 not in hierarchy_biomarkers[key1].keys():
        hierarchy_biomarkers[key1][key2] = []
    hierarchy_biomarkers[key1][key2].append(value)

value_target = 'Age'

for elem in dict_dataset_to_organ_and_view.keys():
    print(elem)

    cols = pd.read_csv('/Users/samuel/Desktop/Dash-Website/data/page1_biomarkers/BiomarkerDatasets/%s.csv' % elem)
    cols_to_use = [elem for elem in cols.columns if elem not in ['Age', 'Age when attended assessment centre', 'Sex', 'eid', 'id'] + ETHNICITY_COLS +  ['Ethnicity.' + elem for elem in ETHNICITY_COLS] + ['ETHNICITY']]

    for column in cols_to_use:

        old_col = column
        column = column.replace('..', '.').replace('.0', '')
        splitted = column.split('.')
        if len(splitted) > 1 :
            feat_name = splitted[0]
            other_col = splitted[1]
        else:
            feat_name = splitted[0]
            other_col = '-'
        final_df = final_df.append({'Main dimension' : dict_dataset_to_organ_and_view[elem][0], 'Subdimension' : dict_dataset_to_organ_and_view[elem][1], 'Sub-subdimension' : dict_dataset_to_organ_and_view[elem][2], 'Feature' : feat_name, 'Sub Field' : other_col, 'Sample Size' : len(cols[old_col].dropna())}, ignore_index = True)
final_df.to_csv('Summary_biomarkers.csv')
