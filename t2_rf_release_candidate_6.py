import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df=pd.read_csv('./girlgeneration(utf8)(1).csv')

df.rename(columns={'T_STANDARD_TICKET_TYPE_NAME':'TICKET_TYPE', 'SEAT_REGION_NAME':'SEAT_TYPE'}, inplace=True)

# Data Processing - convert wrong date time format to the correct one
# Replace "." with empty space in CREATE_DATE and copy data to MY_DATE
df['MY_DATE'] = df.CREATE_DATE.str.replace('.', '', regex=False)

# Apply datetime object with correct format to MY_DATE
df['MY_DATE'] = pd.to_datetime(df['MY_DATE'].str.strip(), format='%Y/%m/%d %p %I:%M:%S')

df = df.sort_values(by='MY_DATE', ascending=True)

for i in df['SEAT_TYPE']:
    exec(i + '_num = []')
    exec(i + '_time = []')

for i in df.groupby(['SEAT_TYPE', 'MY_DATE']):
    # i會印出好長一串, i[0]會得到 ('Floor2Sectionpurple2B', Timestamp('2010-09-18 13:39:48'))
    # 然後這是一個tuple , i[0][0]會得到 'Floor2sectionPurple2B', i[0][1]得到Timestamp, 
    #print(i[0][0], '/', i[0][1], len(i[1])) #zones & date & number of ticks sales
    #print(i[0][1])
    exec(i[0][0] + '_num.append(len(i[1]))')
    time = str(i[0][1]).replace('Timestamp','')
    exec(i[0][0] + '_time.append("' + time + '")')

def get_base(length):
        if length<25:
            return 3
        elif length<50:
            return 15
        elif length<100:
            return 20
        elif length<200:
            return 25
        else:
            return 30

def draw(a, b, c, d, region, colors):
    fig, ax = plt.subplots(a, b, constrained_layout = True, figsize=(c, d))

    tmp_list = []
    for i in sorted(df['SEAT_TYPE'].unique()):
        if i.__contains__(region):
            tmp_list.append(i)

    for n, region in enumerate(tmp_list):
        i = int(n/b)
        j = n%b
        ax[i, j].set_title(region, fontsize='xx-large')
        ax[i, j].plot(eval(region + '_time'), eval(region + '_num'), color=colors[n])
        ax[i, j].xaxis.set_major_locator(ticker.MultipleLocator(base=get_base(len(eval(region + '_time')))))
        plt.setp(ax[i, j].get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    remain = len(tmp_list) % b
    if remain != 0:
        for i in np.arange(remain, b):
            plt.delaxes(ax[a-1, i])

draw(2, 2, 10, 10, 'Floor2Sectionpurple', ['mediumslateblue', 'mediumpurple', 'rebeccapurple', 'blueviolet'])
draw(2, 2, 10, 10, 'Floor2Sectionred', ['red', 'salmon', 'tomato', 'coral'])
draw(2, 3, 15, 10, 'Floor2Sectionyellow', ['gold', 'goldenrod', 'darkkhaki', 'khaki', 'olive'])
draw(2, 5, 25, 10, 'Floor3Sectionyellow',
    ['darkgoldenrod', 'goldenrod', 'gold', 'khaki', 'palegoldenrod', 'darkkhaki', 'wheat', 'tan', 'navajowhite', 'burlywood'])
draw(2, 2, 10, 10, 'FloorB1FloorSection', ['blue', 'darkslateblue', 'mediumblue', 'blueviolet'])

plt.show()
