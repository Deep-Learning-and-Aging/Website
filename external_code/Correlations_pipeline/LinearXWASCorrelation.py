from scipy import stats
import pandas as pd
import numpy as np
path_linear_outputs = '/n/groups/patel/samuel/EWAS/linear_output_paper/'
Environmental = ['Alcohol', 'Diet', 'Education', 'ElectronicDevices',
                 'Employment', 'FamilyHistory', 'Eyesight', 'Mouth',
                 'GeneralHealth', 'Breathing', 'Claudification', 'GeneralPain',
                 'ChestPain', 'CancerScreening', 'Medication', 'Hearing',
                 'Household', 'MentalHealth', 'OtherSociodemographics',
                 'PhysicalActivityQuestionnaire', 'SexualFactors', 'Sleep', 'SocialSupport',
                 'SunExposure', 'EarlyLifeFactors', 'Smoking']
Biomarkers = ['PhysicalActivity', 'HandGripStrength', 'BrainGreyMatterVolumes', 'BrainSubcorticalVolumes',
              'HeartSize', 'HeartPWA', 'ECGAtRest', 'AnthropometryImpedance',
              'UrineBiochemistry', 'BloodBiochemistry', 'BloodCount',
              'EyeAutorefraction', 'EyeAcuity', 'EyeIntraoculaPressure',
              'BraindMRIWeightedMeans', 'Spirometry', 'BloodPressure',
              'AnthropometryBodySize', 'ArterialStiffness', 'CarotidUltrasound',
              'BoneDensitometryOfHeel', 'HearingTest', 'CognitiveFluidIntelligence', 'CognitiveMatrixPatternCompletion',
              'CognitiveNumericMemory', 'CognitivePairedAssociativeLearning', 'CognitivePairsMatching', 'CognitiveProspectiveMemory',
              'CognitiveReactionTime', 'CognitiveSymbolDigitSubstitution', 'CognitiveTowerRearranging', 'CognitiveTrailMaking']

Pathologies = ['medical_diagnoses_%s' % letter for letter in ['A', 'B', 'C', 'D', 'E',
                                                    'F', 'G', 'H', 'I', 'J',
                                                    'K', 'L', 'M', 'N', 'O',
                                                    'P', 'Q', 'R', 'S', 'T',
                                                    'U', 'V', 'W', 'X', 'Y', 'Z']]
All = Environmental + Biomarkers + Pathologies #+ ['Genetics']
organs = ['\\*', '*instances01',
       '*instances1.5x', '*instances23', 'Abdomen', 'AbdomenLiver',
       'AbdomenPancreas', 'Arterial', 'ArterialPulseWaveAnalysis',
       'ArterialCarotids', 'Biochemistry', 'BiochemistryUrine',
       'BiochemistryBlood', 'Brain', 'BrainCognitive', 'BrainMRI', 'Eyes',
       'EyesAll', 'EyesFundus', 'EyesOCT', 'Hearing', 'Heart', 'HeartECG',
       'HeartMRI', 'ImmuneSystem', 'Lungs', 'Musculoskeletal',
       'MusculoskeletalSpine', 'MusculoskeletalHips', 'MusculoskeletalKnees',
       'MusculoskeletalFullBody', 'MusculoskeletalScalars',
       'PhysicalActivity']

path_heritability = '/n/groups/patel/Alan/Aging/Medical_Images/GWAS_hits_Age'
list_df = []
for env_dataset in All:
    print(env_dataset)
    if env_dataset != 'Genetics':
        for organ in organs:
            try : 
                df = pd.read_csv('../linear_output_paper/linear_correlations_%s_%s.csv' % (env_dataset, organ))
                df['env_dataset'] = env_dataset
                list_df.append(df)
            except FileNotFoundError:
                continue
    elif env_dataset == 'Genetics':
        for organ in organs:
            try : 
                df = pd.read_csv(path_heritability + '%s_withGenes.csv' % (organ))
                df['env_dataset'] = env_dataset
                df = df[['Gene', 'BETA', 'P_BOLT_LMM_INF']]
                df = df.rename(columns = {'Gene' : 'env_feature_name', 'BETA' : 'corr_value', 'p_val' : 'P_BOLT_LMM_INF'})
                df['env_dataset'] = 'Genetics'
                df['size_na_dropped'] = 0,
                df['target_dataset_name'] = organ
                list_df.append(df)
            except FileNotFoundError:
                continue
final_df = pd.concat(list_df) 


def Create_data(corr_type, method):
    df_corr_env = pd.DataFrame(columns = ['env_dataset', 'organ_1', 'organ_2', 'corr', 'sample_size'])
    for env_dataset in final_df.env_dataset.drop_duplicates():
        print("Env dataset : ", env_dataset)
        df_env = final_df[final_df.env_dataset == env_dataset]
        for organ_1 in df_env.target_dataset_name.drop_duplicates():
            df_1 = df_env[df_env.target_dataset_name == organ_1].fillna(0)
            n_features_1 = df_1.shape[0]
            significative_df_1 = df_1[df_1['p_val'] < 0.05/n_features_1]
            features_significative_1 = pd.Index(significative_df_1.env_feature_name)
            for organ_2 in df_env.target_dataset_name.drop_duplicates():
                df_2 = df_env[df_env.target_dataset_name == organ_2].fillna(0)
                n_features_2 = df_2.shape[0]
                significative_df_2 = df_2[df_2['p_val'] < 0.05/n_features_2]
                features_significative_2 = pd.Index(significative_df_2.env_feature_name)
                if method == 'Union':
                    significative_features = features_significative_1.union(features_significative_2)
                    df_1_sign = df_1[df_1.env_feature_name.isin(significative_features)].corr_value
                    df_2_sign = df_2[df_2.env_feature_name.isin(significative_features)].corr_value
                elif method == 'Intersection':
                    significative_features = features_significative_1.intersection(features_significative_2)
                    df_1_sign = df_1[df_1.env_feature_name.isin(significative_features)].corr_value
                    df_2_sign = df_2[df_2.env_feature_name.isin(significative_features)].corr_value
                else :
                    df_1_sign = df_1.corr_value
                    df_2_sign = df_2.corr_value
                if len(df_1_sign) <= 1 : 
                    corr = np.nan
                    sample_size = 1
                else :
                    try : 
                        if corr_type == 'Spearman':
                            corr, _ = stats.spearmanr(df_1_sign, df_2_sign)
                        elif corr_type == 'Pearson':
                            corr, _ = stats.pearsonr(df_1_sign, df_2_sign)
                        assert(len(df_1_sign) == len(df_2_sign))
                        sample_size = len(df_1_sign)
                    except ValueError:
                        corr = 0
                df_corr_env = df_corr_env.append({'env_dataset' : env_dataset, 'organ_1' : organ_1, 'organ_2' :organ_2, 'corr' :corr, 'sample_size' : sample_size}, ignore_index = True)
    df_corr_env.to_csv('/n/groups/patel/samuel/EWAS/Correlations/Correlations_%s_%s.csv'% (method, corr_type))


for method in [ 'All' ]:
    for corr_type in ['Pearson', 'Spearman']:
        print(method, corr_type)
        Create_data(corr_type, method)
