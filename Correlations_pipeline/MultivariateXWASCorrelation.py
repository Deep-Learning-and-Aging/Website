from scipy import stats
import pandas as pd
import numpy as np
path_mutlivariate_feat_imps = '/n/groups/patel/samuel/EWAS/feature_importances_paper/'
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
Clusters = []


All = Environmental + Biomarkers + Pathologies #+ ['Genetics']
organs = ['*', '*instances01',
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
def Create_data(corr_type, model):
    df_corr_env = pd.DataFrame(columns = ['env_dataset', 'organ_1', 'organ_2', 'corr', 'sample_size'])
    for env_dataset in All:
        print("Env dataset : ", env_dataset)
        for organ_1 in organs:
            try :
                df_1 = pd.read_csv(path_mutlivariate_feat_imps + 'FeatureImp_%s_%s_%s.csv' % (env_dataset, organ_1, model)).set_index('features').fillna(0)
                print(organ_1)
            except FileNotFoundError as e:
                continue
            for organ_2 in organs:
                try : 
                    df_2 = pd.read_csv(path_mutlivariate_feat_imps + 'FeatureImp_%s_%s_%s.csv' % (env_dataset, organ_2, model)).set_index('features').fillna(0)
                    print(organ_2)
                except FileNotFoundError as e:
                    #print(e)
                    continue
                print(df_1, df_2)
                if corr_type == 'Spearman':
                    corr, _ = stats.spearmanr(df_1.weight, df_2.weight)
                elif corr_type == 'Pearson':
                    corr, _ = stats.pearsonr(df_1.weight, df_2.weight)
                sample_size = len(df_1.weight)
                df_corr_env = df_corr_env.append({'env_dataset' : env_dataset, 'organ_1' : organ_1, 'organ_2' :organ_2, 'corr' :corr, 'sample_size' : sample_size}, ignore_index = True)

    df_corr_env.to_csv('/n/groups/patel/samuel/EWAS/Correlations/CorrelationsMultivariate_%s_%s.csv'% (corr_type, model))
    

for model in ['LightGbm', 'ElasticNet', 'NeuralNetwork']:
    for corr_type in ['Pearson', 'Spearman']:
        print(model, corr_type)
        Create_data(corr_type, model)

