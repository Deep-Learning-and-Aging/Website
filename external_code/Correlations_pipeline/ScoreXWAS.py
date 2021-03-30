import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from scipy import stats
import pandas as pd
import numpy as np
path_linear_outputs = '/n/groups/patel/samuel/EWAS/linear_output_final/'
path_mutlivariate_feat_imps = '/n/groups/patel/samuel/EWAS/not_used_ewas/feature_importances_v2/'
Environmental = ['Clusters_Alcohol', 'Clusters_Diet', 'Clusters_Education', 'Clusters_ElectronicDevices',
                 'Clusters_Employment', 'Clusters_FamilyHistory', 'Clusters_Eyesight', 'Clusters_Mouth',
                 'Clusters_GeneralHealth', 'Clusters_Breathing', 'Clusters_Claudification', 'Clusters_GeneralPain',
                 'Clusters_ChestPain', 'Clusters_CancerScreening', 'Clusters_Medication', 'Clusters_Hearing',
                 'Clusters_Household', 'Clusters_MentalHealth', 'Clusters_OtherSociodemographics',
                 'Clusters_PhysicalActivity', 'Clusters_SexualFactors', 'Clusters_Sleep', 'Clusters_SocialSupport',
                 'Clusters_SunExposure', 'Clusters_EarlyLifeFactors']
Biomarkers = ['Clusters_HandGripStrength', 'Clusters_BrainGreyMatterVolumes', 'Clusters_BrainSubcorticalVolumes',
              'Clusters_HeartSize', 'Clusters_HeartPWA', 'Clusters_ECGAtRest', 'Clusters_AnthropometryImpedance',
              'Clusters_UrineBiochemestry', 'Clusters_BloodBiochemestry', 'Clusters_BloodCount',
              'Clusters_EyeAutorefraction', 'Clusters_EyeAcuity', 'Clusters_EyeIntraocularPressure',
              'Clusters_BraindMRIWeightedMeans', 'Clusters_Spirometry', 'Clusters_BloodPressure',
              'Clusters_AnthropometryBodySize', 'Clusters_ArterialStiffness', 'Clusters_CarotidUltrasound',
              'Clusters_BoneDensitometryOfHeel', 'Clusters_HearingTest', 'Clusters_AnthropometryAllBiomarkers']
Pathologies = ['medical_diagnoses_%s' % letter for letter in ['A', 'B', 'C', 'D', 'E',
                                                    'F', 'G', 'H', 'I', 'J',
                                                    'K', 'L', 'M', 'N', 'O',
                                                    'P', 'Q', 'R', 'S', 'T',
                                                    'U', 'V', 'W', 'X', 'Y', 'Z']]
All = Biomarkers + Environmental + Pathologies #+ ['Genetics']
organs = ['/*', '*instances01',
       '*instances1.5x', '*instances23', 'Abdomen', 'AbdomenLiver',
       'AbdomenPancreas', 'Arterial', 'ArterialPulseWaveAnalysis',
       'ArterialCarotids', 'Biochemistry', 'BiochemistryUrine',
       'BiochemistryBlood', 'Brain', 'BrainCognitive', 'BrainMRI', 'Eyes',
       'EyesAll', 'EyesFundus', 'EyesOCT', 'Hearing', 'Heart', 'HeartECG',
       'HeartMRI', 'ImmuneSystem', 'Lungs', 'Musculoskeletal',
       'MusculoskeletalSpine', 'MusculoskeletalHips', 'MusculoskeletalKnees',
       'MusculoskeletalFullBody', 'MusculoskeletalScalars',
       'PhysicalActivity']

t = pd.read_csv('/n/groups/patel/Alan/Aging/Medical_Images/data/RESIDUALS_bestmodels_instances_Age_test.csv').set_index('id')
print(t.columns)
path_multivariate_preds = '/n/groups/patel/samuel/EWAS/preds_paper/'
organs = ['\*','*instances01','*instances1.5x','*instances23','Abdomen','AbdomenLiver','AbdomenPancreas','Arterial','ArterialPulseWaveAnalysis','ArterialCarotids','Biochemistry','BiochemistryUrine','BiochemistryBlood','Brain','BrainCognitive','BrainMRI','Eyes','EyesAll','EyesFundus','EyesOCT','Hearing','Heart','HeartECG','HeartMRI','ImmuneSystem','Lungs','Musculoskeletal','MusculoskeletalSpine','MusculoskeletalHips','MusculoskeletalKnees','MusculoskeletalFullBody','MusculoskeletalScalars','PhysicalActivity']

def Create_score_table(algo, step = 'test'):
    print("STARTING STEP : %s" % step)
    df_corr_env = pd.DataFrame(columns = ['env_dataset', 'organ', 'std', 'r2', 'sample_size'])
    for env_dataset in Biomarkers + Environmental + Pathologies:
        print("Env dataset : ", env_dataset)
        for organ in organs:
            print(organ)
            try :
                df = pd.read_csv(path_multivariate_preds + 'Predictions_%s_%s_%s_%s.csv' % (env_dataset, organ, algo, step)).set_index('id')
                full = df.join(t[[organ.replace('\\', '')]])
                sample_size = len(full['pred'])
                r2 =  r2_score(full[organ.replace('\\', '')], full['pred'])
                std = np.std([r2_score(full[full.outer_fold == fold][organ.replace('\\', '')], full[full.outer_fold == fold]['pred']) for fold in range(10)])
                if env_dataset in Environmental:
                    subset = 'Environmental'
                elif env_dataset in Pathologies:
                    subset = 'Pathologies'
                elif env_dataset in Biomarkers:
                    subset = 'Biomarkers'
                df_corr_env = df_corr_env.append({'sample_size' : sample_size, 'env_dataset' : env_dataset, 'organ' : organ, 'std' : std, 'r2' : r2, 'subset' : subset}, ignore_index = True)
            except FileNotFoundError as e:
                print(e)
                continue
    df_corr_env.to_csv('/n/groups/patel/samuel/EWAS/Scores/Scores_%s_%s.csv' % (algo, step))
    return df_corr_env


df_corr_env = Create_score_table('LightGbm', step = 'test')
df_corr_env = Create_score_table('ElasticNet', step = 'test')
df_corr_env = Create_score_table('NeuralNetwork', step = 'test')
    
