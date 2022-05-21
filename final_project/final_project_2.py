import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.ticker as tkr
import matplotlib.patches as mpatches
from matplotlib.axis import Axis

# Define a custom formatter so values in the thousands are converted (e.g. 50k)
def numfmt(x, pos):
    s = '{}k'.format(int(x / 1000))
    return s

xfmt = tkr.FuncFormatter(numfmt)

df = pd.read_csv("https://raw.githubusercontent.com/cliftonleesps/602_adv_prog_tech/main/final_project/df_out_2.csv")

df.info()

#print(df.shape)


fields = pd.read_csv("https://raw.githubusercontent.com/cliftonleesps/602_adv_prog_tech/main/final_project/Most-Recent-Cohorts-Field-of-Study_2.csv")

fields = fields.replace('PrivacySuppressed', np.nan)
fields['EARN_MDN_HI_1YR'] = pd.to_numeric(fields['EARN_MDN_HI_1YR'])
fields['EARN_MDN_HI_2YR'] = pd.to_numeric(fields['EARN_MDN_HI_2YR'])
fields['EARN_NE_MDN_3YR'] = pd.to_numeric(fields['EARN_NE_MDN_3YR'])

# filter for CS major and bachelor degrees at public colleges
fields = fields[(fields['CIPCODE'] == 1101) & (fields['CREDLEV'] == 3)]
fields = fields[fields['CONTROL'] == 'Public']

print(fields.shape)




df_states = df.copy()
df_states = df_states[df_states['ACCREDAGENCY'].isnull() == False]
df_states = df_states[(df_states['NPT4_PUB'].isnull() == False) & (df_states['NPT4_PUB'].isna() == False)]
df_states = df_states[df_states['CONTROL'] == 1]
df_states = df_states[df_states['STABBR'].isin(['NY', 'PA','DE','VA','NJ','CT','RI','MA'])]
df_states = df_states[['STABBR']]

# Set general theme options
sns.set_theme() #style="whitegrid", palette="pastel")
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)

result = df_states.groupby(['STABBR'])['STABBR'].size().sort_values(ascending=True)

barplot = sns.barplot(x = result.index, y = result.values)
barplot.set_xlabel("States",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
barplot.set_ylabel("Number of Colleges", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
barplot.set_title('Public Colleges in Select States', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
#barplot.bar_label(barplot.containers[0])

plt.show()




# clean up the roomboard column
df_histogram = df
df_histogram['ROOMBOARD_ON'] = df_histogram['ROOMBOARD_ON'].fillna(0)

# filter out rows with empty tuition
df_histogram = df_histogram[df_histogram['TUITIONFEE_IN'].isna() == False]

print(df_histogram[['TUITIONFEE_IN']].median())

sns.set_theme(style="whitegrid", palette="pastel",rc={"axes.spines.left": False, "axes.spines.right": False, "axes.spines.top": False})
histogram = sns.histplot(data=df_histogram,bins=50, x="TUITIONFEE_IN", color="lightgreen")
histogram.set_xlabel("Tuition",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram.set_ylabel("Frequency", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram.set_title('Public College Tuition for Select States', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
histogram.xaxis.grid(False) 
histogram.xaxis.set_major_formatter(xfmt)
plt.show()








df_control1 = df[(df['ROOMBOARD_ON'] > 0.0) & (df['TUITIONFEE_IN'] > 0.0) & (df['BOOKSUPPLY'] > 0.0) & (df['OTHEREXPENSE_ON'] > 0.0) & (df['CONTROL'] == 1)]
df_control2 = df[(df['ROOMBOARD_ON'] > 0.0) & (df['TUITIONFEE_IN'] > 0.0) & (df['BOOKSUPPLY'] > 0.0) & (df['OTHEREXPENSE_ON'] > 0.0) & (df['CONTROL'] == 2)]
df_control3 = df[(df['ROOMBOARD_ON'] > 0.0) & (df['TUITIONFEE_IN'] > 0.0) & (df['BOOKSUPPLY'] > 0.0) & (df['OTHEREXPENSE_ON'] > 0.0) & (df['CONTROL'] == 3)]


df_cost_chart = pd.DataFrame( { 'Tuition (In State)' : [df_control1['TUITIONFEE_IN'].median(), df_control2['TUITIONFEE_IN'].median(), df_control3['TUITIONFEE_IN'].median()],
                                'Book' : [df_control1['BOOKSUPPLY'].median(), df_control2['BOOKSUPPLY'].median(), df_control3['BOOKSUPPLY'].median()],
                                'Dorm' : [df_control1['ROOMBOARD_ON'].median(), df_control2['ROOMBOARD_ON'].median(), df_control3['ROOMBOARD_ON'].median()],
                                'Other' : [df_control1['OTHEREXPENSE_ON'].median(), df_control2['OTHEREXPENSE_ON'].median(), df_control3['OTHEREXPENSE_ON'].median()]},
                              index = ['Public','Private nonprofit','Private for-profit'])


df_cost_sea = df_cost_chart.copy()
df_cost_sea['Book'] = df_cost_sea['Book'] + df_cost_sea['Tuition (In State)']
df_cost_sea['Dorm'] = df_cost_sea['Dorm'] + df_cost_sea['Book']
df_cost_sea['Other'] = df_cost_sea['Other'] + df_cost_sea['Dorm']



# Seaborn bar chart

sns.barplot(data=df_cost_sea, x=['Public','Private nonprofit','Private for-profit'], y="Other", color='gray')
sns.barplot(data=df_cost_sea, x=['Public','Private nonprofit','Private for-profit'], y="Dorm", color='green')
sns.barplot(data=df_cost_sea, x=['Public','Private nonprofit','Private for-profit'], y="Book", color='skyblue')
b = sns.barplot(data=df_cost_sea, x=['Public','Private nonprofit','Private for-profit'], y="Tuition (In State)", color='orange')

b.set_xlabel("College Type",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
b.set_ylabel("Cost ", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
b.set_title('Median Cost of College', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
b.yaxis.set_major_formatter(xfmt)
b.xaxis.grid(False)
b.yaxis.grid(True)
patch_other = mpatches.Patch(color='gray', label='Other')
patch_dorm = mpatches.Patch(color='green', label='Dorm')
patch_book = mpatches.Patch(color='skyblue', label='Book')
patch_tuition = mpatches.Patch(color='orange', label='Tuition')
plt.legend(handles=[patch_tuition, patch_dorm, patch_book, patch_other], loc = 2, bbox_to_anchor = (0.85,1))

plt.show()







# replace all privacy suppressed values
df = df.replace('PrivacySuppressed', np.nan)  

# convert the below columns to numeric
df['GRAD_DEBT_MDN'] = pd.to_numeric(df['GRAD_DEBT_MDN'])
df['CUML_DEBT_N'] = pd.to_numeric(df['CUML_DEBT_N'])
# subset for nearby, public colleges
df = df[df['ACCREDAGENCY'].isnull() == False]
df = df[(df['NPT4_PUB'].isnull() == False) & (df['NPT4_PUB'].isna() == False)]
df = df[df['CONTROL'] == 1]  # public
df = df[df['SCH_DEG'] == 3]  # bachelor's primary degree type awarded
df = df[df['STABBR'].isin(['NY', 'PA','DE','VA','NJ','CT','RI','MA'])]


jdf = df.join(fields.set_index('UNITID'), on='UNITID', rsuffix = "_fields")


# filter out rows where the median earnings are NaN
jdf = jdf[jdf['EARN_NE_MDN_3YR'].isna() == False]

# convert to float
jdf = jdf[jdf['EARN_NE_MDN_3YR'].isna() == False]
jdf['EARN_NE_MDN_3YR'] = jdf['EARN_NE_MDN_3YR'].astype(float)


fig = px.scatter(jdf,
                 x="EARN_NE_MDN_3YR",
                 y="GRAD_DEBT_MDN",
                 color="STABBR",
                 hover_data=['INSTNM'],
                 size='EARN_NE_MDN_3YR')

o = fig.update_xaxes(range=[40000,110000])
o = fig.update_yaxes(range=[10000, 30000])

o = fig.update_layout(title={ 'text': '<span style="font-size: 2em;"><b>Median Annual Earnings Versus Median Debt</b></span>',
                              'y':0.95,
                              'x':0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                      legend_title_text='State',
                      yaxis_title="<b>Median Debt at Graduation</b>",
                      xaxis_title="<b>Median Earnings 3 Years After Graduation</b>"
                      )
fig.show()






histogram = sns.histplot(data=jdf,bins=50, x="IPEDSCOUNT1", color="lightgreen")
histogram.set_xlabel("Cohort Count",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram.set_ylabel("Frequency", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram.set_title('Graduating Class Size 2018', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
histogram.xaxis.grid(False) 
plt.show()

print ("\n\n")

histogram_2019 = sns.histplot(data=jdf,bins=50, x="IPEDSCOUNT2", color="lightgreen")
histogram_2019.set_xlabel("Cohort Count",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram_2019.set_ylabel("Frequency", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram_2019.set_title('Graduating Class Size 2019', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
histogram_2019.xaxis.grid(False) 


plt.show()




jdf['ratio'] = jdf['EARN_NE_MDN_3YR'] / jdf['NPT4_PUB']

print(jdf.sort_values(ascending=False,by='EARN_NE_MDN_3YR')[['EARN_NE_MDN_3YR', 'NPT4_PUB','ratio', 'INSTNM']].head(20).to_markdown())

print("\n\n")




As many know, college attendance costs have risen so quickly in the last few decades, many families face a difficult decision of where to send students without incurring an overwhelming amount of debt.

The Department of Education publishes its College Scorecard, explaining university attributes including financial.

We'll be using the College Scorecard dataset (in CSV format) and the Pandas library to clean, join and chart various financial perspectives. The main goal of this notebook is to find the public, four year university where the graduates earn the most while having the least amount of graduating debt.

We find that in the general Nort East and Mid Atlantic states, computer science graduates from the University of Connecticut at Waterbury earn ten times more than their debt three years after graduation.

