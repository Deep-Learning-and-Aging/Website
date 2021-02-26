import numpy as np
import pandas as pd

import io
import pandas as pd
import boto3
from botocore.client import Config
import os
import base64
import matplotlib.image as mpimg
from app import app

import os
try :
    path_credentials = '/Users/samuel/Downloads/Alan_accessKeys.csv'
    creds = pd.read_csv(path_credentials)
    access_key = creds.iloc[0]['Access key ID']
    secret_key = creds.iloc[0]['Secret access key']
    bucket_name = 'age-prediction-site'
except FileNotFoundError:
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    bucket_name = 'age-prediction-site'
print("SECRET KEY IS ", secret_key)
print("ACCESS KEY IS ", access_key)
## S3 credentials
client = boto3.client('s3',
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      config=Config(signature_version='s3v4'))


def load_csv(id_path, **kwargs):
    obj = client.get_object(Bucket=bucket_name, Key=id_path)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()), **kwargs)
    return df

def read_img(id_path, remote = True):
    if remote :
        obj = client.get_object(Bucket=bucket_name, Key=id_path)
        return mpimg.imread(io.BytesIO(obj['Body'].read()), format="jpg")
    else :
        id_path = './' + app.get_asset_url(id_path)
        return mpimg.imread(id_path)

def load_npy(id_path, remote = True):
    if remote :
        obj = client.get_object(Bucket=bucket_name, Key=id_path)
        return np.load(io.BytesIO(obj['Body'].read()))
    else :
        id_path = './' + app.get_asset_url(id_path)
        return np.load(id_path)


def encode_img_s3(id_path, remote = True):
    if remote:
        obj = client.get_object(Bucket=bucket_name, Key=id_path)
        return base64.b64encode(obj['Body'].read()).decode('ascii')
    else :
        id_path = './' + app.get_asset_url(id_path)
        return base64.b64encode(open(id_path, 'rb').read()).decode('ascii')


def list_obj(id_path, remote = True):
    if remote :
        try :
            res = [elem['Key'] for elem in client.list_objects_v2(Bucket=bucket_name, Prefix = id_path)['Contents']]
            return res
        except KeyError :
            return []
    else :
        id_path = './' + app.get_asset_url(id_path)
        return glob.glob(id_path + '*')

## Score of all models
path_score_scalar = 'page2_predictions/Performances/PERFORMANCES_tuned_alphabetical_eids_Age_test.csv'
score = load_csv(path_score_scalar)

## Load heritability
filename_heritabilty = 'page11_GWASHeritability/Heritability/GWAS_heritabilities_Age.csv'
heritability = load_csv(filename_heritabilty)[['h2', 'h2_sd', 'Organ']]


empty_graph = {
    "layout": {
        "xaxis": {
            "visible": False
        },
        "yaxis": {
            "visible": False
        },
        "annotations": [
            {
                "text": "No data",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 28
                }
            }
        ]
    }
}
ETHNICITY_COLS = ['Do_not_know', 'Prefer_not_to_answer', 'NA', 'White', 'British',
       'Irish', 'White_Other', 'Mixed', 'White_and_Black_Caribbean',
       'White_and_Black_African', 'White_and_Asian', 'Mixed_Other', 'Asian',
       'Indian', 'Pakistani', 'Bangladeshi', 'Asian_Other', 'Black',
       'Caribbean', 'African', 'Black_Other', 'Chinese', 'Other_ethnicity',
       'Other']


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
    'PhysicalActivity' : ('PhysicalActivity', 'FullWeek', 'Scalars'),
    'Demographics' : ('Demographics', 'All', 'Scalars')
}

dict_organ_view_transf_to_id = { v : k for k, v in dict_dataset_to_organ_and_view.items()}

hierarchy_biomarkers = dict()
for key1, key2, value in dict_dataset_to_organ_and_view.values():
    if key1 not in hierarchy_biomarkers.keys():
        hierarchy_biomarkers[key1] = {}
    if key2 not in hierarchy_biomarkers[key1].keys():
        hierarchy_biomarkers[key1][key2] = []
    hierarchy_biomarkers[key1][key2].append(value)


def get_dataset_options(list_):
    list_label_value = []
    for elem in list_:
        d = {'value' : elem, 'label' : elem}
        list_label_value.append(d)
    return list_label_value

def f(x):
    if x <= 0:
        x1 = 255*(x + 1)
        x1 = round(x1, 5)
        return 'rgba(%s, %s, %s, 0.85)' % (255, int(x1), int(x1))
    else :
        x2 = 255*(1 - x)
        x2 = round(x2, 5)
        return 'rgba(%s, %s, %s, 0.85)' % (int(x2), int(x2), 255)

def get_colorscale(df):
    min = df.min().min()
    max = df.max().max()
    abs = np.abs(min/(min - max))
    if abs > 1 :
        colorscale =  [[0, f(min)],
                       [1, f(max)]]
    else:
        colorscale =  [[0, f(min)],
                        [abs, 'rgba(255, 255, 255, 0.85)'],
                        [1, f(max)]]
    return colorscale
