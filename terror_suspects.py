import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os


def valid_yes_no(answer):
    while answer not in ['y','n']:
        answer = input('Please Answer "y" for yes or "n" for no: ')
    return answer

def terror(row,weight):
    if row == True:
        return weight
    else:
        return 0

def ages(row,weights,param):
    if row > param[0] and row<param[1]:
        return weights[2]
    elif row >param[1] and row <param[2]:
        return weights[1]
    else:
        return 0

def male(row,weight):
    if row == 'm':
        return weight
    else:
        return 0

def terrorist_contact(row,weights,param):
    row = int(row)
    if row < param[0]:
        return weights[0]
    elif row >param[0] and row <param[1]:
        return weights[1]
    elif row >param[1] and row<param[2]:
        return weights[2]
    elif row > param[2]:
        return weights[3]

#special_tag
def special_tag_terror(row,weights):
    if row == 'terrorist_superfamily':
        return weights[2]
    elif row == 'terrorist_boss_wife':
        return weights[1]
    elif row == 'terrorist_boss':
        return weights[0]
    else:
        return 0

def match_phone(data_calls, arr):
    for id_num in arr:
        #if id_num in arr:
            data_calls['suspect_match'] = data_calls['id_from'] == id_num
            data_calls['suspect_match'] = data_calls['id_to'] == id_num
    return data_calls



people = pd.read_csv('people.csv')

calls_to_terror = people['call_group'].str.contains('terror')
number_of_terror_calls = people[calls_to_terror]['call_group'].apply(lambda x: x.split('_')[2])


#parameters:
age_paras = [16,40,50]
terrorist_contact_params = [5,30,70]

#Weights:
terror_weight = 25
age_weights = [0,5,10]
gender_male_weight = 10
terrorist_contact_weights = [0,10,20,30]
special_tags_weights = [10,15,25]
max_score = terror_weight + age_weights[2] + gender_male_weight + terrorist_contact_weights[3] + special_tags_weights[2]
print(max_score)


print('Hello Inspector\n')
print('In our tool you can find details of suspects in terror.')
print('This tool work according to diverse information. \nwe created for you a main column called: "chance_of_a_terrorist". ')
print('This column contains parameters and weights. Each one of the suspects get final score range ("0" for innocent and "100" for Probably a terrorist).')
print('The parameters are:\n')
print('1. known as a Terrorist -  \t weight: {}'.format(terror_weight))
print('2. Suspect age - \t Under {al} - weight: {l}.\n\t\t\t\t\t  Between {al} to {am} - weight: {h}.\n\t\t\t\t\t  Between {am} to {amh} - weight: {m}.\n\t\t\t\t\t  Above {amh} - weight: {l} '.format(l=age_weights[0], m=age_weights[1], h=age_weights[2],al=age_paras[0],am=age_paras[1],amh=age_paras[2]))
print('3. Male suspect - \t weight: {}'.format(gender_male_weight))
print('4. Terrorist_contact according to connection volume  - \t Under {al} connections - weight: {l}.\n\t\t\t\t\t  Between {al} to {am} connections - weight: {ml}.\n\t\t\t\t\t  Between {am} to {amh} connections - weight: {mh}.\n\t\t\t\t\t  Above {amh} connections - weight: {h}.'.format(l=terrorist_contact_weights[0], ml=terrorist_contact_weights[1], mh=terrorist_contact_weights[2], h=terrorist_contact_weights[3], al=terrorist_contact_params[0], am=terrorist_contact_params[1], amh=terrorist_contact_params[2]))
print('5. Terror family connection (Special tags) - \t Terrorist_superfamily - weight: {h}.\n\t\t\t\t\t\t\t\t\t\t\t\t Terrorist_boss_wife - weight: {m}.\n\t\t\t\t\t\t\t\t\t\t\t\t Terrorist_boss - weight: {l}\n'.format(h=special_tags_weights[2], m=special_tags_weights[1], l=special_tags_weights[0]))

inspector_change = input('Inspector would you like to change weights? (y or n): <<<press only n - if i had more time it was interactive>>>')
inspector_change = valid_yes_no(inspector_change)
if inspector_change == 'y':
    print('\nPlease set the weight according to your demand: ')
    print('###PLEASE PAY ATTENTION DO NOT CROSS ABOVE 100 (weights field)### ')
    change_known_as_terror = input('Would like to change - known as a Terrorist weight? (y or n) ')
    change_known_as_terror = valid_yes_no(change_known_as_terror)



#Terrorist - True
people['terror_weight'] = people['is_terrorist'].apply(lambda row: terror(row, terror_weight))
#Between ages
people['age_weight'] = people['age'].apply(lambda row: ages(row,age_weights,age_paras))
#Gender - male
people['male_weight'] = people['gender'].apply(lambda row: male(row,gender_male_weight))
#Terrorists Contact
people['terror_contact_weight'] = number_of_terror_calls.apply(lambda row: terrorist_contact(row,terrorist_contact_weights, terrorist_contact_params))
people['terror_contact_weight'].fillna(0, inplace=True)
#Special tags
people['special_tag_weight'] = people['special_tag'].apply(lambda row: special_tag_terror(row, special_tags_weights))
#creting the summary column of the all other fields (written in lines above)
people['chance_of_a_terrorist'] = people.iloc[:, 12:17].sum(axis=1)


#get only the id for the suspects that got scoore bigger then 60:
biggest_chance_for_terror = people.loc[people['chance_of_a_terrorist'] > 60]

id_biggest_chance_for_terror = biggest_chance_for_terror['id']
arr_id_chance_to_terror = np.asarray(biggest_chance_for_terror['id'])





cwd = os.getcwd()
entries = os.listdir(cwd + '\phonecalls')

df_suspect_match_summary_table = pd.DataFrame()
for file in entries:
    calls = pd.read_csv(cwd + '\phonecalls\\' + file)
    calls['end_date'] = pd.to_datetime(calls['end_date'])
    calls['start_date'] = pd.to_datetime(calls['start_date'])
    calls['Call_duration'] = calls['end_date'] - calls['start_date']

    df_suspect_match = match_phone(calls, arr_id_chance_to_terror)
    df_suspect_match.head()
    df_suspect_match = df_suspect_match.loc[df_suspect_match['suspect_match'] == True]
    df_suspect_match_summary_table = df_suspect_match_summary_table.append(df_suspect_match)



print('saving files as csv')
biggest_chance_for_terror.to_csv('people_chance_terror.csv', index=False)
df_suspect_match_summary_table.to_csv('phonecalls_match.csv', index=False)
