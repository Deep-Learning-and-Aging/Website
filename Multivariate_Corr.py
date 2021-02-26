from scipy import stats
import pandas as pd
import numpy as np
path_mutlivariate_feat_imps = '/n/groups/patel/samuel/EWAS/feature_importances_paper/'
Environmental = ['Clusters_Alcohol', 'Clusters_Diet', 'Clusters_Education', 'Clusters_ElectronicDevices',
                 'Clusters_Employment', 'Clusters_FamilyHistory', 'Clusters_Eyesight', 'Clusters_Mouth',
                 'Clusters_GeneralHealth', 'Clusters_Breathing', 'Clusters_Claudification', 'Clusters_GeneralPain',
                 'Clusters_ChestPain', 'Clusters_CancerScreening', 'Clusters_Medication', 'Clusters_Hearing',
                 'Clusters_Household', 'Clusters_MentalHealth', 'Clusters_OtherSociodemographics',
                 'Clusters_PhysicalActivityQuestionnaire', 'Clusters_SexualFactors', 'Clusters_Sleep', 'Clusters_SocialSupport',
                 'Clusters_SunExposure', 'Clusters_EarlyLifeFactors', 'Clusters_Smoking']
Biomarkers = ['Clusters_PhysicalActivity', 'Clusters_HandGripStrength', 'Clusters_BrainGreyMatterVolumes', 'Clusters_BrainSubcorticalVolumes',
              'Clusters_HeartSize', 'Clusters_HeartPWA', 'Clusters_ECGAtRest', 'Clusters_AnthropometryImpedance',
              'Clusters_UrineBiochemistry', 'Clusters_BloodBiochemistry', 'Clusters_BloodCount',
              'Clusters_EyeAutorefraction', 'Clusters_EyeAcuity', 'Clusters_EyeIntraoculaPressure',
              'Clusters_BraindMRIWeightedMeans', 'Clusters_Spirometry', 'Clusters_BloodPressure',
              'Clusters_AnthropometryBodySize', 'Clusters_ArterialStiffness', 'Clusters_CarotidUltrasound',
              'Clusters_BoneDensitometryOfHeel', 'Clusters_HearingTest', 'Clusters_CognitiveFluidIntelligence', 'Clusters_CognitiveMatrixPatternCompletion',
	      'Clusters_CognitiveNumericMemory', 'Clusters_CognitivePairedAssociativeLearning', 'Clusters_CognitivePairsMatching', 'Clusters_CognitiveProspectiveMemory',
	      'Clusters_CognitiveReactionTime', 'Clusters_CognitiveSymbolDigitSubstitution', 'Clusters_CognitiveTowerRearranging', 'Clusters_CognitiveTrailMaking']
Pathologies = ['medical_diagnoses_%s' % letter for letter in ['A', 'B', 'C', 'D', 'E',
                                                    'F', 'G', 'H', 'I', 'J',
                                                    'K', 'L', 'M', 'N', 'O',
                                                    'P', 'Q', 'R', 'S', 'T',
                                                    'U', 'V', 'W', 'X', 'Y', 'Z']]
Clusters = []


All = Environmental + Biomarkers + Pathologies #+ ['Genetics']
organs = ['\*', '*instances01', '*instances1.5x', '*instances23', 'Abdomen' , 'AbdomenLiver' , 'AbdomenPancreas' , 'Arterial' , 'ArterialCarotids' , 'ArterialPulseWaveAnalysis' , 'Biochemistry' , 'BiochemistryBlood' , 'BiochemistryUrine' , 'Brain' , 'BrainCognitive' , 'BrainMRI' , 'Eyes' , 'EyesAll' , 'EyesFundus' , 'EyesOCT' , 'Hearing' , 'Heart' , 'HeartECG' , 'HeartMRI' , 'ImmuneSystem' , 'Lungs' , 'Musculoskeletal' , 'MusculoskeletalFullBody' , 'MusculoskeletalHips' , 'MusculoskeletalKnees' , 'MusculoskeletalScalars' , 'MusculoskeletalSpine' , 'PhysicalActivity']

path_heritability = '/n/groups/patel/Alan/Aging/Medical_Images/GWAS_hits_Age'
def Create_data(corr_type, model):
    df_corr_env = pd.DataFrame(columns = ['env_dataset', 'organ_1', 'organ_2', 'corr', 'sample_size'])
    for env_dataset in All:
        print("Env dataset : ", env_dataset)
        for organ_1 in organs:
            try :
                df_1 = pd.read_csv(path_mutlivariate_feat_imps + 'FeatureImp_%s_%s_%s.csv' % (env_dataset, organ_1, model)).set_index('features').fillna(0)
            except FileNotFoundError as e:
                continue
            for organ_2 in organs:
                try :
                    df_2 = pd.read_csv(path_mutlivariate_feat_imps + 'FeatureImp_%s_%s_%s.csv' % (env_dataset, organ_2, model)).set_index('features').fillna(0)
                except FileNotFoundError as e:
                    #print(e)
                    continue
                try :
                    if corr_type == 'Spearman':
                        corr, _ = stats.spearmanr(df_1.weight, df_2.weight)
                    elif corr_type == 'Pearson':
                        corr, _ = stats.pearsonr(df_1.weight, df_2.weight)
                except ValueError:
                    commun_indexes = df_1.weight.index.intersection(df_2.weight.index))
                    if corr_type == 'Spearman':
                        corr, _ = stats.spearmanr(df_1.weight.loc[commun_indexes], df_2.weight.loc[commun_indexes])
                    elif corr_type == 'Pearson':
                        corr, _ = stats.pearsonr(df_1.weight.loc[commun_indexes], df_2.weight.loc[commun_indexes])

                sample_size = len(df_1.weight)
                df_corr_env = df_corr_env.append({'env_dataset' : env_dataset, 'organ_1' : organ_1, 'organ_2' :organ_2, 'corr' :corr, 'sample_size' : sample_size}, ignore_index = True)

    df_corr_env.to_csv('/n/groups/patel/samuel/EWAS/Correlations/CorrelationsMultivariate_%s_%s.csv'% (corr_type, model))


for model in ['LightGbm', 'ElasticNet', 'NeuralNetwork']:
    for corr_type in ['Pearson', 'Spearman']:
        Create_data(corr_type, model)
