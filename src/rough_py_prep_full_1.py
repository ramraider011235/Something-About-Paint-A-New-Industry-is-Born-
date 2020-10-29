import pandas as pd
# pd.options.display.float_format = '{:,.2f}'.format
pd.options.display.max_columns = 50
pd.options.display.max_rows = 999
import numpy as np 
import json
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
matplotlib.rcParams.update({'font.size' : 16, 'font.family' : 'sans'})
import scipy as sp
import scipy.stats as stats
import scipy.optimize as sco
from scipy.optimize import minimize
from sklearn.linear_model import LinearRegression
import seaborn as sns
sns.set()
from bs4 import BeautifulSoup as bs
import requests
import requests_html
from urllib.request import urlopen
from datetime import date, datetime, timedelta
from IPython.display import IFrame
import warnings
warnings.filterwarnings('ignore')

data = []
def imports():
    data_lst0 = ['assumptions', 'census', 'paintCare_CO', 'paint_collected', 'paint_processed', 'profit_loss','proforma', 'states', 'total_cost', 'weekly_kpi']
    for n in range(10):
        data.append(pd.read_csv('/home/gordon/galvanize/Capstone_1/data/' + str(data_lst0[n]) + '.csv'))
        
def clean(clean_lst0):
    for clean in clean_lst0:
        columns = clean.columns
        cols = [column.replace(' ', '_') for column in columns]
        cols = [col.replace('.','') for col in cols]
        cols = [col.replace('(','') for col in cols]
        cols = [col.replace(')','') for col in cols]
        cols = [col.replace(':','') for col in cols]
        clean.columns = [col.lower() for col in cols]
    for clean in clean_lst0:
        clean.fillna(0, inplace = True)
imports()
clean(data)   
############################################################################################################################################

assumptions = data[0]
# assumptions

############################################################################################################################################

census = data[1][['year','total_pop']]
census['total_pop'] = census['total_pop'].astype(float)
census['epa_est_sold_gal'] = census['total_pop'] * 2.4
census['paintCare_collect_gal'] = census['epa_est_sold_gal'] * 0.05
census['potential_mkt'] = census['paintCare_collect_gal'] * 3.8

x = np.arange(len(census['epa_est_sold_gal']))
step = int((int(census['epa_est_sold_gal'].max()) - int(census['total_pop'].min())) / 10)
y = np.arange(int(census['total_pop'].min()) - step, int(census['epa_est_sold_gal'].max()) + step, step)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, ylabel='Dollars In Billions $') 
census[['epa_est_sold_gal', 'total_pop']].plot(kind = 'bar', ax=ax, width = 2)
ax.set_xticks(x)
ax.set_xticklabels(census['year'], rotation = 60)
ax.set_yticks(y)
ax.set_title('Paint Collection: Potential US Market.')
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
sns.set(style='darkgrid', context='talk', palette='Dark2')
# plt.tight_layout()
# plt.show()


x1 = np.arange(len(census['potential_mkt']))
step1 = int((int(census['potential_mkt'].max()) - int(census['paintCare_collect_gal'].min())) / 10)
y1 = np.arange(int(census['paintCare_collect_gal'].min()) - step1, int(census['potential_mkt'].max())+step1,step1)

fig = plt.figure(figsize=(15, 11))
ax1 = fig.add_subplot(111, ylabel='Price in $')    
census[['potential_mkt', 'paintCare_collect_gal']].plot(kind = 'bar', ax=ax1, width = 2)
ax1.set_xticks(x1)
ax1.set_xticklabels(census['year'], rotation = 60)
ax1.set_yticks(y1)
ax1.set_title('Potential Market Per EPA Figures:')
ax1.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
sns.set(style='darkgrid', context='talk', palette='Dark2')
# plt.tight_layout()
# plt.show()

census.head();

############################################################################################################################################

paintcare_co = data[2]

x = np.arange(len(paintcare_co['2019']))
step = int((int(paintcare_co['2019'].max()) - int(paintcare_co['2015'].min())) / 10)
y = np.arange(int(paintcare_co['2015'].min()) - step, int(paintcare_co['2019'].max()) + step, step)

fig = plt.figure(figsize=(18, 11))
ax = fig.add_subplot(111, ylabel = 'Dollars in $10million') 
paintcare_co[['2015', '2016', '2017', '2018', '2019']].plot(kind = 'bar', ax=ax, width = .75, align = 'edge')
ax.set_xticks(x)
ax.set_xticklabels(paintcare_co['co_record'], rotation = 30)
ax.set_yticks(y)
ax.set_title('PaintCare Record: CO')
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
sns.set(style='darkgrid', context='talk', palette='Dark2')
# plt.tight_layout()
# plt.show()


pc2 = pd.DataFrame()
pc2['mean'] = paintcare_co.mean(axis = 1)
pc2['median'] = paintcare_co.median(axis = 1)
pc2['min'] = paintcare_co.min(axis = 1)
pc2['max'] = paintcare_co.max(axis = 1)
pc2['std'] = paintcare_co.std(axis = 1)
pc2 = pc2.astype(float)

x1 = np.arange(len(pc2['mean']))
step1 = int((int(pc2['max'].max()) - int(pc2['min'].min())) / 10)
y1 = np.arange(int(pc2['min'].min()) - step1, int(pc2['max'].max()) + step1, step1)

fig = plt.figure(figsize=(18, 11))
ax1 = fig.add_subplot(111, ylabel = 'Dollars in $10 million') 
pc2[['mean', 'median', 'min', 'max', 'std']].plot(kind = 'bar', ax = ax1, width = .75, align = 'edge')
ax1.set_xticks(x)
ax1.set_xticklabels(paintcare_co['co_record'], rotation = 30)
ax1.set_yticks(y)
ax1.set_title('PaintCare - CO')
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
sns.set(style='darkgrid', context='talk', palette='Dark2')
# plt.tight_layout()
# plt.show()

print(pc2 , paintcare_co)
############################################################################################################################################

paint_collected = data[3]
date = list(paint_collected.columns[1:])
date.insert(0, 'date')
paint_collected = data[3].transpose()
paint_collected['date'] = date
paint_collected.sort_values('date')

paint_collected.columns = list(paint_collected.iloc[0])
columns = paint_collected.columns
cols = [column.replace(' ', '_') for column in columns]
paint_collected.columns = [col.lower() for col in cols]
paint_collected = paint_collected.drop('paint_collected_gallons')

x = np.arange(len(paint_collected['co']))
y = np.arange(0, int(paint_collected['co'].max()) + 250, 1000)
fig = plt.figure(figsize=(25, 15))
ax = fig.add_subplot(111, ylabel = 'Company Paint Collected: By State', xlabel = 'Weekly Report') 
paint_collected[['co', 'wa', 'az']].plot(kind = 'bar', ax = ax, width = .7, align = 'edge')
ax.set_xticks(x)
ax.set_xticklabels(paint_collected['date'], rotation = 70)
ax.set_yticks(y)
ax.set_title('Company Collection Records:')
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
sns.set(style='darkgrid', context='talk', palette='Dark2')
# plt.tight_layout()
# plt.show()


x1 = np.arange(len(paint_collected['total_collected']))
y1 = np.arange(int(paint_collected['total_collected'].min()) - 500, 
               int(paint_collected['total_collected'].max()) + 500, 1000)
fig = plt.figure(figsize=(25, 15))
ax1 = fig.add_subplot(111, ylabel = 'Company Paint Collected: Total Collection', xlabel = 'Weekly Report') 
paint_collected['total_collected'].plot(kind = 'bar', ax = ax1, width = 0.5, align = 'edge')
ax1.set_xticks(x1)
ax1.set_xticklabels(paint_collected['date'], rotation = 70)
ax1.set_yticks(y1)
ax1.set_title('Company Collection Records:')
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
sns.set(style='darkgrid', context='talk', palette='Dark2')
# plt.tight_layout()
# plt.show()


x2 = np.arange(len(paint_collected['total_collected']))
y2 = np.arange(0, int(paint_collected['total_collected'].max()) + 250, 1000)
fig = plt.figure(figsize=(25, 15))
ax2 = fig.add_subplot(111, ylabel = 'Company Paint Collected', xlabel = 'Weekly Report') 
paint_collected[['co', 'wa', 'az', 'total_collected']].plot(ax = ax2, linewidth=3.0)
ax2.set_xticks(x2)
ax2.set_xticklabels(paint_collected['date'], rotation = 70)
ax2.set_yticks(y2)
ax2.set_title('Company Collection Records:')
plt.grid(which="major", color='k', linestyle='-.', linewidth = 0.5)
sns.set(style='darkgrid', context='talk', palette='Dark2')
# plt.tight_layout()
# plt.show()

############################################################################################################################################

paint_processed = data[4]

date1 = list(paint_processed.columns[1:])
date1.insert(0, 'date')
paint_processed = data[4].transpose()
paint_processed['date'] = date1
paint_processed.sort_values('date')

paint_processed.columns = list(paint_processed.iloc[0])
columns = paint_processed.columns
cols = [column.replace(' ', '_') for column in columns]
cols = [col.replace('(', '') for col in cols]
cols = [col.replace(')', '') for col in cols]
paint_processed.columns = [col.lower() for col in cols]
paint_processed = paint_processed.drop('total_paint_processing')


x = np.arange(len(paint_processed['paint_shipped_gallons']))
y = np.arange(0, int(paint_processed['paint_shipped_gallons'].max()) + 250, 1000)
fig = plt.figure(figsize=(20, 13))
ax = fig.add_subplot(111, ylabel = 'Company Paint Collected', xlabel = 'Weekly Report') 
paint_processed[['paint_processed_gallons', 'paint_packaged_gallons', 
                 'paint_shipped_gallons']].plot(ax = ax, linewidth=3.0)
ax.set_xticks(x)
ax.set_xticklabels(paint_collected['date'], rotation = 70)
ax.set_yticks(y)
ax.set_title('Company Collection Records:')
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
sns.set(style='darkgrid', context='talk', palette='Dark2')
# plt.tight_layout()
# plt.show()


x = np.arange(len(paint_processed['paint_shipped_gallons']))
y = np.arange(0, int(paint_processed['paint_shipped_gallons'].max()) + 250, 1000)
fig = plt.figure(figsize=(25, 13))
ax1 = fig.add_subplot(111, ylabel = 'Company Paint Collected', xlabel = 'Weekly Report') 
paint_processed[['paint_processed_gallons', 'paint_packaged_gallons', 
                 'paint_shipped_gallons']].plot(kind = 'bar', width = .75, align = 'edge', ax = ax1)
ax1.set_xticks(x)
ax1.set_xticklabels(paint_collected['date'], rotation = 70)
ax1.set_yticks(y)
ax1.set_title('Company Collection Records:')
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
sns.set(style='darkgrid', context='talk', palette='Dark2')
# plt.tight_layout()
# plt.show()

############################################################################################################################################

profit_loss = data[5].transpose()

profit_loss.columns = list(profit_loss.iloc[0])
columns = profit_loss.columns
cols = [column.replace(' ', '') for column in columns]
profit_loss.columns = [col.lower() for col in cols]
profit_loss = profit_loss.drop(['category'])
profit_loss['annual'] = ['2017', '2018', '2019']

x = np.arange(len(profit_loss['totalincome']))
step = int((int(profit_loss['totalincome'].max()) - int(profit_loss['uncategorized'].min())) / 10)
y = np.arange(0, int(profit_loss['totalincome'].max()) + .0, step)

fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(111, ylabel='Dollars $', xlabel = 'Annual') 
profit_loss[['totalincome', 'cogs', 'grossprofit', 'totalexpenses',
             'netoperatingincome']].plot(kind = 'bar', ax = ax, width = .85, align = 'edge');
ax.set_xticks(x)
ax.set_xticklabels(profit_loss['annual'], rotation = 0)
ax.set_yticks(y)
ax.set_title('Profit Loss')
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
sns.set(style='darkgrid', context='talk', palette='Dark2')
# plt.tight_layout()
# plt.show()

x1 = np.arange(len(profit_loss['wholesalesales']))
step1 = int((int(profit_loss['wholesalesales'].max()) / 10))
y1 = np.arange(0, int(profit_loss['wholesalesales'].max()), step1)

fig = plt.figure(figsize=(20, 10))
ax1 = fig.add_subplot(111, ylabel='Dollars $', xlabel = 'Annual' )
profit_loss[['recycling', 'wholesalesales', 'collectionfees(az)', 
             'uncategorized']].plot(kind = 'bar', ax = ax1, width = .85, align = 'edge');
ax1.set_xticks(x1)
ax1.set_xticklabels(profit_loss['annual'], rotation = 0)
ax1.set_yticks(y1)
ax1.set_title('Sources of Revenue')
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
sns.set(style='darkgrid', context='talk', palette='Dark2')
# plt.tight_layout()
# plt.show()

profit_loss

############################################################################################################################################

proforma = data[6].drop([2, 5])

proforma = proforma[['state','pop_000','total_sold','state_recycle','green_recycle','green_product']]
proforma = proforma.drop([6,7,8])

x = np.arange(len(proforma['state']))
step = int(95000000 / 15)
y = np.arange(0, 95000000, step)

fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(111, ylabel='Dollars $', xlabel = 'Annual') 
proforma[['pop_000', 'total_sold', 'state_recycle', 'green_recycle', 
          'green_product']].plot(kind = 'bar', ax = ax, width = .85, align = 'edge');
ax.set_xticks(x)
ax.set_xticklabels(proforma['state'], rotation = 0)
ax.set_yticks(y)
ax.set_title('Profit Loss')
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
sns.set(style='darkgrid', context='talk', palette='Dark2')
# plt.tight_layout()
# plt.show()

proforma;

###################################################################################################################################

state = data[7]

state.at[51, 'state'] = 'Total'
state.at[50, 'rank_1-50'] = 51

state = state.drop(['2010_pop', '%_to_total', 'potential_gals_paint',
                    'potential_rev_@_$15_gal', 'gross_profit_est_65%', 'rank_1-50'], axis = 1)
state = state.sort_values(by = '2018_pop', ascending = False)
state['rank'] = np.arange(0, 52)
state['2018_pop'] = state['2018_pop'].astype(float)
state.set_index('rank', inplace = True)

state['sold'] = state['2018_pop'] * 2.4
state['collected'] = state['sold'] * 0.05
state['revenue'] = state['collected'] * 3.8
state['company'] = state['revenue'] * 0.35

state.head()

###################################################################################################################

total_cost = data[8]
total_cost.set_index('category')

###################################################################################################################

weekly_kpi = data[9]
weekly_kpi

##############################################################v#########/home/gordon/galvanize/Capstone_1/data############################################

plt.show()

###################################################################################################################
def imports():
    data = []
    data_lst_1 = ['gs_pl_2015', 'gs_pl_2016', 'gs_pl_2017', 'gs_pl_2018']
    for n in range(4):
        data.append(pd.read_csv('/home/gordon/galvanize/Capstone_1/data/' + str(data_lst_1[n]) + '.csv'))
    return data
        
def clean():
    clean_lst0 = imports()
    for clean in clean_lst0:
        columns = clean.columns
        cols = [column.replace(' ', '_') for column in columns]
        cols = [col.replace('.','') for col in cols]
        cols = [col.replace('(','') for col in cols]
        cols = [col.replace(')','') for col in cols]
        cols = [col.replace('-','') for col in cols]
        cols = [col.replace(':','') for col in cols]
        cols = [col.replace('__','_') for col in cols]
        clean.columns = [col.lower() for col in cols]
    for clean in clean_lst0:
        clean.fillna(0.0, inplace = True)
    return clean_lst0
data = clean() 

def finish():
    pl_2015, pl_2016, pl_2017, pl_2018 = data[0], data[1], data[2], data[3]
    lst_of_lst_0 = [pl_2015, pl_2016, pl_2017, pl_2018]
    pl2015, pl2016, pl2017, pl2018 = (pl_2015[pl_2015.columns[0]]), (pl_2016[pl_2016.columns[0]]), (pl_2017[pl_2017.columns[0]]), (pl_2018[pl_2018.columns[0]])
    lst_of_lst = [pl2015, pl2016, pl2017, pl2018]

    one = set(pl2015) & set(pl2016)
    two = one & set(pl2017)
    three = two & set(pl2018)
    three = list(three)

    for idx, num in enumerate(lst_of_lst):
        for i, n in enumerate(num):
            if n not in three:
                lst_of_lst_0[idx] = lst_of_lst_0[idx].drop(i)
    print(len(three))
    pl_2015, pl_2016, pl_2017, pl_2018 = lst_of_lst_0[0], lst_of_lst_0[1], lst_of_lst_0[2], lst_of_lst_0[3]
    return pl_2015, pl_2016, pl_2017, pl_2018
finish = finish()

def check():
    print(len(finish[0]), len(finish[1]), len(finish[2]), len(finish[3]))
    f2015, f2016, f2017, f2018 = finish[0], finish[1], finish[2], finish[3]
check()

#################################################################################################################################################

# f2015.head()
# f2016.head()
# f2017.head()
# f2018.head()

category = list(f2015['january_december_2015'])

df = pd.DataFrame()
df['category'] = category
df['2015'] = f2015['total']
df['2016'] = f2016['total']
df['2017'] = f2017['total']
df['2018'] = f2018['total']
df.plot(figsize = (12,9))
plt.show()

df['max'] = round(df.max(axis = 1), 2)
df['mean'] = round(df.mean(axis = 1), 2)
df['median'] = round(df.median(axis = 1), 2)
df['min'] = round(df.min(axis = 1), 2)
df['std'] = round(df.std(axis = 1), 2)

df.fillna(0.0, inplace = True)
# df.to_csv('data/here.csv')
df