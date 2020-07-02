
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
