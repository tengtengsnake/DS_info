import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

df=pd.read_csv('./girlgeneration(utf8)(1).csv')
df.rename(columns={'T_STANDARD_TICKET_TYPE_NAME':'TICKET_TYPE', 'SEAT_REGION_NAME':'SEAT_TYPE'}, inplace=True)

female=df.groupby(['SEX']).get_group('female') #女
female_member=female.groupby(['TICKET_TYPE']).get_group('member') #女會員
female_non_member=female.groupby(['TICKET_TYPE']).get_group('non-member') #女非會員
male=df.groupby(['SEX']).get_group('male') #男
male_member=male.groupby(['TICKET_TYPE']).get_group('member') #男會員
male_non_member=male.groupby(['TICKET_TYPE']).get_group('non-member') #男非會員

member_or_not=['male-member', 'female-member', 'male-non-member', 'female-non-member']
list_all=[len(male_member), len(female_member), len(male_non_member), len(female_non_member)]
color=['lightblue', 'red', 'lightblue', 'red']
x = np.arange(len(member_or_not))
plt.figure(figsize=(8, 8))
plt.bar(x, list_all, width=0.3, align='center', color=color)
plt.title('Concert-sales-analysis', fontsize='xx-large')
plt.xlabel('Membership', fontsize='xx-large')
plt.xticks(x, member_or_not, fontsize='large')
plt.ylabel('Sales', fontsize='xx-large')
red_patch = mpatches.Patch(color='red',  label='female')
blue_patch = mpatches.Patch(color='lightblue',  label='male')
plt.legend(loc='upper right', fontsize='large', handles=[red_patch, blue_patch])
plt.tight_layout()

female_member_list=[]
female_non_member_list=[]
male_member_list=[]
male_non_member_list=[]
for i in df.groupby(['SEAT_TYPE', 'SEX', 'TICKET_TYPE'], group_keys=False):
    #print(i[0][0], '/', i[0][1], '/', i[0][2], ': ', len(i[1]))
    if (i[0][0] == 'Floor3Sectionyellow3E' and
            i[0][1] == 'female' and
            i[0][2] == 'member'):
        female_member_list.append(len(i[1]))
        female_non_member_list.append(0)
        #print('Floor3Sectionyellow3E / female / non-member: 0')
        continue
    if i[0][1] == 'female':
        if i[0][2] == 'member':
            female_member_list.append(len(i[1]))
        else:
            female_non_member_list.append(len(i[1]))
    else:
        if i[0][2] == 'member':
            male_member_list.append(len(i[1]))
        else:
            male_non_member_list.append(len(i[1]))

xticks_regions=sorted(df['SEAT_TYPE'].unique())
x=np.arange(len(female_member_list))

#Stacked bar chart
#member_list
plt.figure(figsize=(10, 10))
plt.title('Member sales by region', fontsize='xx-large')
plt.xlabel('Regions', fontsize='xx-large')
plt.ylabel('Sales', fontsize='xx-large')
plt.xticks(x, xticks_regions, rotation=45, ha='right')
plt.yticks(np.arange(50, 550, 25))
plt.bar(x, male_member_list, label='male')
plt.bar(x, female_member_list, bottom=male_member_list, color='red', label='female')
plt.legend()

#Stacked bar chart
#non_member_list
plt.figure(figsize=(10, 10))
plt.title('Non-member sales by region', fontsize='xx-large')
plt.xlabel('Regions', fontsize='xx-large')
plt.ylabel('Sales', fontsize='xx-large')
plt.xticks(x, xticks_regions, rotation=45, ha='right')
plt.yticks(np.arange(0, 100, 5))
plt.bar(x, male_non_member_list, label='male')
plt.bar(x, female_non_member_list, bottom=male_non_member_list, color='red', label='female')
plt.legend()

plt.show()
