import numpy as np

ETHNICITY_COLS = ['Do_not_know', 'Prefer_not_to_answer', 'NA', 'White', 'British',
       'Irish', 'White_Other', 'Mixed', 'White_and_Black_Caribbean',
       'White_and_Black_African', 'White_and_Asian', 'Mixed_Other', 'Asian',
       'Indian', 'Pakistani', 'Bangladeshi', 'Asian_Other', 'Black',
       'Caribbean', 'African', 'Black_Other', 'Chinese', 'Other_ethnicity',
       'Other']

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
        return 'rgba(%s, %s, %s, 0.85)' % (255, x1, x1)
    else :
        x2 = 255*(1 - x)
        x2 = round(x2, 5)
        return 'rgba(%s, %s, %s, 0.85)' % (x2, x2, 255)

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
