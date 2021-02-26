import numpy as np
import pandas as pd
import glob
import os
final_df = pd.DataFrame(columns = ['Main dimension', 'Subdimension', 'Sub-subdimension', 'CorrelationVersusElasticNet', 'CorrelationVersusLightGBM', 'CorrelationVersusNeuralNetwork', 'ElasticNetVersusLightGBM', 'ElasticNetVersusNeuralNetwork', 'LightGBMVersusNeuralNetwork'])
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
    'BloodBiochemestry' : ('Biochemistry', 'Blood', 'Scalars'),
    'UrineBiochemestry' : ('Biochemistry', 'Urine', 'Scalars'),
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
for corr_method in ['Spearman', 'Pearson']:
    for value_organ in hierarchy_biomarkers.keys():
        for value_view in hierarchy_biomarkers[value_organ]:
            for value_transformation in hierarchy_biomarkers[value_organ][value_view]:

                score_model = score[(score['organ'] == value_organ) & (score['view'] == value_view) & (score['transformation'] == value_transformation)][['architecture', 'R-Squared_all', 'N_all']]
                score_lightgbm = score_model[score_model['architecture'] == 'LightGBM']['R-Squared_all']
                score_nn = score_model[score_model['architecture'] == 'NeuralNetwork']['R-Squared_all']
                score_elasticnet = score_model[score_model['architecture'] == 'ElasticNet']['R-Squared_all']
                sample_size = score_model[score_model['architecture'] == 'ElasticNet']['N_all']


                list_df = glob.glob(path_feat_imps + 'FeatureImp_%s_%s_%s_%s_*.csv' % (value_target, value_organ, value_view, value_transformation))
                list_df_sd = glob.glob(path_feat_imps + 'FeatureImp_sd_%s_%s_%s_%s_*.csv' % (value_target, value_organ, value_view, value_transformation))
                for idx, elem in enumerate(list_df):
                    df_new = pd.read_csv(elem, na_filter = False).set_index('features')
                    _, _, _, _, _, model = os.path.basename(elem).split('_')
                    model = model.replace('.csv', '').replace('LightGbm', 'LightGBM')
                    list_models.append(model)
                    df_new.columns = [model]
                    if idx == 0:
                        df = df_new
                    else :
                        df = df.join(df_new)
                df = df.replace('', 0).fillna(0).astype(float)
                df_abs = df.abs()/df.abs().sum()

                ## Sort by mean of 3 models :
                # df['mean'] = df.mean(axis = 1)
                # df = df.sort_values('mean', ascending = True).drop(columns = ['mean'])

                ## Sort by best model :
                if score_lightgbm.values > score_nn.values and score_lightgbm.values > score_elasticnet.values:
                    df_abs = df_abs.sort_values('LightGBM')
                elif score_nn.values > score_lightgbm.values and score_nn.values > score_elasticnet.values:
                    df_abs = df_abs.sort_values('NeuralNetwork')
                else :
                    df_abs = df_abs.sort_values('ElasticNet')


                df_abs.index = df_abs.index.str.replace('.0$', '', regex = True)

                if len(df_abs.columns) < 4:
                    print(value_organ, value_view, value_transformation)
                    print([elem for elem in list_models if elem not in df_abs.columns])
                else:

                    matrix = df_abs[sorted(df_abs.columns)].corr(method=corr_method.lower())
                    matrix.index.name = 'Corr'
                    matrix = matrix.round(3)
                    final_df = final_df.append({'Organ' : value_organ,
                                     'View' : value_view,
                                     'Transformation' : value_transformation,
                                     'Correlation_ElasticNet' : matrix.loc['Correlation'].loc['ElasticNet'],
                                     'Correlation_LightGBM' : matrix.loc['Correlation'].loc['LightGBM'],
                                     'Correlation_NeuralNetwork' : matrix.loc['Correlation'].loc['NeuralNetwork'],
                                     'ElasticNet_LightGBM' : matrix.loc['ElasticNet'].loc['LightGBM'],
                                     'ElasticNet_NeuralNetwork' : matrix.loc['ElasticNet'].loc['NeuralNetwork'],
                                     'LightGBM_NeuralNetwork' : matrix.loc['LightGBM'].loc['NeuralNetwork']},
                                     ignore_index = True)
    final_df.to_csv('Correlations_%s_Age_scalars_feature_importances.csv' % corr_method)
