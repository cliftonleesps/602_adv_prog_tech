import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def filter_non_numeric(dataframe, convert_columns):
    for c in convert_columns:
        dataframe = dataframe[dataframe[c] != 'PrivacySuppressed']
        dataframe = dataframe[dataframe[c].isna() == False]
        dataframe[c] = pd.to_numeric(dataframe[c])
    return dataframe


#df = pd.read_csv("https://raw.githubusercontent.com/cliftonleesps/602_adv_prog_tech/main/final_project/df_out.csv")
df = pd.read_csv("df_out.csv")


df_states = df
df_states = df_states[df_states['ACCREDAGENCY'].isnull() == False]
df_states = df_states[df_states['CONTROL'] == 1]
df_states = df_states[df_states['STABBR'].isin(['NY', 'PA','DE','VA','NJ','CT','RI','MA'])]
df_states = df_states[['STABBR']]


# Group by states, sort by count
result = df_states.groupby(['STABBR'])['STABBR'].size().sort_values(ascending=True)
seaborn.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)¶

# Plot 1 - Barplot by states
sns.set_theme() #style="whitegrid", palette="pastel")
barplot = sns.barplot(x = result.index, y = result.values)
barplot.set_xlabel("States",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
barplot.set_ylabel("Number of Colleges", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
barplot.set_title('Public Colleges in Select States', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
barplot.bar_label(barplot.containers[0])

plt.show()


# clean up the roomboard column
df_histogram = df
df_histogram['ROOMBOARD_ON'] = df_histogram['ROOMBOARD_ON'].fillna(0)

# filter out rows with empty tuition
df_histogram = df_histogram[df_histogram['TUITIONFEE_IN'].isna() == False]

def numfmt(x, pos): # your custom formatter function: divide by 100.0
    s = '{}k'.format(x / 1000)
    return s

import matplotlib.ticker as tkr     # has classes for tick-locating and -formatting
xfmt = tkr.FuncFormatter(numfmt)    # create your custom formatter function




# Plot 2 - histogram of in state tuition
sns.set_theme(style="whitegrid", palette="pastel",rc={"axes.spines.left": False, "axes.spines.right": False, "axes.spines.top": False})
histogram = sns.histplot(data=df_histogram,bins=50, x="TUITIONFEE_IN", color="lightgreen")
histogram.set_xlabel("Tuition",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram.set_ylabel("Frequency", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram.set_title('Public College Tuition for Select States', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
histogram.xaxis.grid(False) 
#histogram.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:.0f}k'))
histogram.xaxis.set_major_formatter(xfmt)
plt.show()


# Plot 3 - Scatterplot of average faculty salary vs 
df_scatter = df
df_scatter = df_scatter[df_scatter['ACCREDAGENCY'].isnull() == False]
df_scatter = df_scatter[df_scatter['CONTROL'] == 1]
df_scatter = df_scatter[df_scatter['STABBR'].isin(['NY', 'PA','DE','VA','NJ','CT','RI','MA'])]
df_scatter = df_scatter[df_scatter['AVGFACSAL'].isna() == False]
df_scatter = df_scatter[df_scatter['NPT4_PUB'].isna() == False]

sns.scatterplot(data=df_scatter, x="AVGFACSAL", y="NPT4_PUB", hue="STABBR")
plt.show()



# Plot 4 - Barchart of costs
df_control1 = df[(df['ROOMBOARD_ON'] > 0.0) & (df['TUITIONFEE_IN'] > 0.0) & (df['BOOKSUPPLY'] > 0.0) & (df['OTHEREXPENSE_ON'] > 0.0) & (df['CONTROL'] == 1)]
df_control2 = df[(df['ROOMBOARD_ON'] > 0.0) & (df['TUITIONFEE_IN'] > 0.0) & (df['BOOKSUPPLY'] > 0.0) & (df['OTHEREXPENSE_ON'] > 0.0) & (df['CONTROL'] == 2)]
df_control3 = df[(df['ROOMBOARD_ON'] > 0.0) & (df['TUITIONFEE_IN'] > 0.0) & (df['BOOKSUPPLY'] > 0.0) & (df['OTHEREXPENSE_ON'] > 0.0) & (df['CONTROL'] == 3)]

df_cost_chart = pd.DataFrame( { 'Tuition (In State)' : [df_control1['TUITIONFEE_IN'].median(), df_control2['TUITIONFEE_IN'].median(), df_control3['TUITIONFEE_IN'].median()],
                                'Book' : [df_control1['BOOKSUPPLY'].median(), df_control2['BOOKSUPPLY'].median(), df_control3['BOOKSUPPLY'].median()],
                                'Dorm' : [df_control1['ROOMBOARD_ON'].median(), df_control2['ROOMBOARD_ON'].median(), df_control3['ROOMBOARD_ON'].median()],
                                'Other' : [df_control1['OTHEREXPENSE_ON'].median(), df_control2['OTHEREXPENSE_ON'].median(), df_control3['OTHEREXPENSE_ON'].median()]},
                              index = ['Public','Private nonprofit','Private for-profit'])

# Matplot lib bar chart
df_cost_chart.plot(kind='bar', stacked=True, color=['orange', 'skyblue', 'green', 'gray'])
plt.xticks(rotation=0)
plt.title('Median Costs of College')
plt.xlabel('College Type')
plt.show()

# Seaborn bar chart
sns.barplot(data=df_cost_chart, x=['Public','Private nonprofit','Private for-profit'], y="Tuition (In State)", color='darksalmon')
sns.barplot(data=df_cost_chart, x=['Public','Private nonprofit','Private for-profit'], y="Dorm", color='lightgrey')
sns.barplot(data=df_cost_chart, x=['Public','Private nonprofit','Private for-profit'], y="Other", color='darkblue')
sns.barplot(data=df_cost_chart, x=['Public','Private nonprofit','Private for-profit'], y="Book", color='lightblue')

plt.show()

