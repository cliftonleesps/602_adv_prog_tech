import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.ticker as tkr
from matplotlib.axis import Axis
import matplotlib.patches as mpatches

def filter_non_numeric(dataframe, convert_columns):
    for c in convert_columns:
        dataframe = dataframe[dataframe[c] != 'PrivacySuppressed']
        dataframe = dataframe[dataframe[c].isna() == False]
        dataframe[c] = pd.to_numeric(dataframe[c])
    return dataframe


df = pd.read_csv("https://raw.githubusercontent.com/cliftonleesps/602_adv_prog_tech/main/final_project/df_out.csv")
#df = pd.read_csv("df_out.csv")


df_states = df
df_states = df_states[df_states['ACCREDAGENCY'].isnull() == False]
df_states = df_states[df_states['CONTROL'] == 1]
df_states = df_states[df_states['STABBR'].isin(['NY', 'PA','DE','VA','NJ','CT','RI','MA'])]
df_states = df_states[['STABBR']]


# Group by states, sort by count
result = df_states.groupby(['STABBR'])['STABBR'].size().sort_values(ascending=True)
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)

# Plot 1 - Barplot by states (Seaborn)
sns.set_theme() #style="whitegrid", palette="pastel")
barplot = sns.barplot(x = result.index, y = result.values)
barplot.set_xlabel("States",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
barplot.set_ylabel("Number of Colleges", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
barplot.set_title('Public Colleges in Select States', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
barplot.bar_label(barplot.containers[0])

plt.show()

# Plot 1 - Barplot by states (Matplotlib)
bars = plt.bar(result.index, result.values, color=['blue','burlywood', 'seagreen', 'indianred', 'slateblue', 'sienna', 'orchid', 'grey'])
plt.bar_label(bars)
plt.title("Public Colleges in Select States", fontdict= { 'fontsize': 16, 'fontweight':'bold'}, loc='center')
plt.xlabel("States",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
plt.ylabel("Number of Colleges", fontdict= { 'fontsize': 12, 'fontweight':'bold'})

# grids
ax = plt.gca()
ax.yaxis.grid(True)
ax.xaxis.grid(False)

plt.show()





# clean up the roomboard column
df_histogram = df
df_histogram['ROOMBOARD_ON'] = df_histogram['ROOMBOARD_ON'].fillna(0)

# filter out rows with empty tuition
df_histogram = df_histogram[df_histogram['TUITIONFEE_IN'].isna() == False]

def numfmt(x, pos):
    s = '{}k'.format(int(x / 1000))
    return s

xfmt = tkr.FuncFormatter(numfmt)




# Plot 2 - histogram of in state tuition (Seaborn)
sns.set_theme(style="whitegrid", palette="pastel",rc={"axes.spines.left": False, "axes.spines.right": False, "axes.spines.top": False})
histogram = sns.histplot(data=df_histogram,bins=50, x="TUITIONFEE_IN", color="lightgreen")
histogram.set_xlabel("Tuition",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram.set_ylabel("Frequency", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram.set_title('Public College Tuition for Select States', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
histogram.xaxis.grid(False) 
histogram.xaxis.set_major_formatter(xfmt)
plt.show()


# Plot 2 - histogram of in state tuition (Matplotlib)
fig, ax = plt.subplots()
plt.hist(df_histogram['TUITIONFEE_IN'], bins=50, color="lightgreen")
plt.title("Public Colleges Tuition for Select States", fontdict= { 'fontsize': 16, 'fontweight':'bold'}, loc='center')
plt.xlabel("Tuition",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
plt.ylabel("Frequency", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
Axis.set_major_formatter(ax.xaxis, xfmt)
Axis.sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)

# Plot 1 - Barplot by states (Seaborn)
sns.set_theme() #style="whitegrid", palette="pastel")
barplot = sns.barplot(x = result.index, y = result.values)
barplot.set_xlabel("States",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
barplot.set_ylabel("Number of Colleges", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
barplot.set_title('Public Colleges in Select States', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
barplot.bar_label(barplot.containers[0])

plt.show()

# Plot 1 - Barplot by states (Matplotlib)
bars = plt.bar(result.index, result.values, color=['blue','burlywood', 'seagreen', 'indianred', 'slateblue', 'sienna', 'orchid', 'grey'])
plt.bar_label(bars)
plt.title("Public Colleges in Select States", fontdict= { 'fontsize': 16, 'fontweight':'bold'}, loc='center')
plt.xlabel("States",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
plt.ylabel("Number of Colleges", fontdict= { 'fontsize': 12, 'fontweight':'bold'})

# grids
ax = plt.gca()
ax.yaxis.grid(True)
ax.xaxis.grid(False)

plt.show()





# clean up the roomboard column
df_histogram = df
df_histogram['ROOMBOARD_ON'] = df_histogram['ROOMBOARD_ON'].fillna(0)

# filter out rows with empty tuition
df_histogram = df_histogram[df_histogram['TUITIONFEE_IN'].isna() == False]

def numfmt(x, pos):
    s = '{}k'.format(int(x / 1000))
    return s

xfmt = tkr.FuncFormatter(numfmt)




# Plot 2 - histogram of in state tuition (Seaborn)
sns.set_theme(style="whitegrid", palette="pastel",rc={"axes.spines.left": False, "axes.spines.right": False, "axes.spines.top": False})
histogram = sns.histplot(data=df_histogram,bins=50, x="TUITIONFEE_IN", color="lightgreen")
histogram.set_xlabel("Tuition",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram.set_ylabel("Frequency", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram.set_title('Public College Tuition for Select States', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
histogram.xaxis.grid(False) 
histogram.xaxis.set_major_formatter(xfmt)
plt.show()


# Plot 2 - histogram of in state tuition (Matplotlib)
fig, ax = plt.subplots()
plt.hist(df_histogram['TUITIONFEE_IN'], bins=50, color="lightgreen")
plt.title("Public Colleges Tuition for Select States", fontdict= { 'fontsize': 16, 'fontweight':'bold'}, loc='center')
plt.xlabel("Tuition",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
plt.ylabel("Frequency", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
Axis.set_major_formatter(ax.xaxis, xfmt)
Axis.sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)

# Plot 1 - Barplot by states (Seaborn)
sns.set_theme() #style="whitegrid", palette="pastel")
barplot = sns.barplot(x = result.index, y = result.values)
barplot.set_xlabel("States",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
barplot.set_ylabel("Number of Colleges", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
barplot.set_title('Public Colleges in Select States', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
barplot.bar_label(barplot.containers[0])

plt.show()

# Plot 1 - Barplot by states (Matplotlib)
bars = plt.bar(result.index, result.values, color=['blue','burlywood', 'seagreen', 'indianred', 'slateblue', 'sienna', 'orchid', 'grey'])
plt.bar_label(bars)
plt.title("Public Colleges in Select States", fontdict= { 'fontsize': 16, 'fontweight':'bold'}, loc='center')
plt.xlabel("States",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
plt.ylabel("Number of Colleges", fontdict= { 'fontsize': 12, 'fontweight':'bold'})

# grids
ax = plt.gca()
ax.yaxis.grid(True)
ax.xaxis.grid(False)

plt.show()





# clean up the roomboard column
df_histogram = df
df_histogram['ROOMBOARD_ON'] = df_histogram['ROOMBOARD_ON'].fillna(0)

# filter out rows with empty tuition
df_histogram = df_histogram[df_histogram['TUITIONFEE_IN'].isna() == False]

def numfmt(x, pos):
    s = '{}k'.format(int(x / 1000))
    return s

xfmt = tkr.FuncFormatter(numfmt)




# Plot 2 - histogram of in state tuition (Seaborn)
sns.set_theme(style="whitegrid", palette="pastel",rc={"axes.spines.left": False, "axes.spines.right": False, "axes.spines.top": False})
histogram = sns.histplot(data=df_histogram,bins=50, x="TUITIONFEE_IN", color="lightgreen")
histogram.set_xlabel("Tuition",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram.set_ylabel("Frequency", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
histogram.set_title('Public College Tuition for Select States', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
histogram.xaxis.grid(False) 
histogram.xaxis.set_major_formatter(xfmt)
plt.show()


# Plot 2 - histogram of in state tuition (Matplotlib)
fig, ax = plt.subplots()
plt.hist(df_histogram['TUITIONFEE_IN'], bins=50, color="lightgreen")
plt.title("Public Colleges Tuition for Select States", fontdict= { 'fontsize': 16, 'fontweight':'bold'}, loc='center')
plt.xlabel("Tuition",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
plt.ylabel("Frequency", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
Axis.set_major_formatter(ax.xaxis, xfmt)
# grids
ax = plt.gca()
ax.yaxis.grid(True)
ax.xaxis.grid(False)

plt.show()




# Plot 3 - Scatterplot of average faculty salary vs net price (Seaborn)
df_scatter = df
df_scatter = df_scatter[df_scatter['ACCREDAGENCY'].isnull() == False]
df_scatter = df_scatter[df_scatter['CONTROL'] == 1]
df_scatter = df_scatter[df_scatter['STABBR'].isin(['NY', 'PA','DE','VA','NJ','CT','RI','MA'])]
df_scatter = df_scatter[df_scatter['AVGFACSAL'].isna() == False]
df_scatter = df_scatter[df_scatter['NPT4_PUB'].isna() == False]

scatterplot = sns.scatterplot(data=df_scatter, x="AVGFACSAL", y="NPT4_PUB", hue="STABBR")
scatterplot.set_xlabel("Faculty Salary Per Month",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
scatterplot.set_ylabel("Net College Price Per Year ", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
scatterplot.set_title('Average Net College Price Compared to Average Monthly Teaching Salaries', fontdict= { 'fontsize': 16, 'fontweight':'bold'})
scatterplot.xaxis.set_major_formatter(xfmt)
scatterplot.yaxis.set_major_formatter(xfmt)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.show()


# Plot 3 - Scatterplot of average faculty salary vs net price (Matplotlib)
colors = { 'CT' : 'blue',
           'DE' : 'burlywood',
           'MA' : 'seagreen',
           'NJ' : 'indianred',
           'NY' : 'slateblue',
           'PA' : 'sienna',
           'RI' : 'orchid',
           'VA' : 'grey'}

patch_CT = mpatches.Patch(color='blue', label='CT')
patch_DE = mpatches.Patch(color='burlywood', label='DE')
patch_MA = mpatches.Patch(color='seagreen', label='MA')
patch_NJ = mpatches.Patch(color='indianred', label='NJ')
patch_NY = mpatches.Patch(color='slateblue', label='NY')
patch_PA = mpatches.Patch(color='sienna', label='PA')
patch_RI = mpatches.Patch(color='orchid', label='RI')
patch_VA = mpatches.Patch(color='grey', label='VA')
           
fig, ax = plt.subplots()
scatter = ax.scatter(df_scatter["AVGFACSAL"], df_scatter["NPT4_PUB"], s=10, c=df_scatter['STABBR'].map(colors), cmap=colors, label="dffdf")
plt.title("Average Net College Price Compared to Average Monthly Teaching Salaries", fontdict= { 'fontsize': 16, 'fontweight':'bold'}, loc='center')
plt.xlabel("Faculty Salary Per Month",  fontdict= { 'fontsize': 12, 'fontweight':'bold'})
plt.ylabel("Net College Price Per Year", fontdict= { 'fontsize': 12, 'fontweight':'bold'})
Axis.set_major_formatter(ax.xaxis, xfmt)
Axis.set_major_formatter(ax.yaxis, xfmt)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)
ax.spines[['left','right','bottom','top']].set_color('black')
ax.set_facecolor('white')
u, d = np.unique(df_scatter["STABBR"], return_inverse=True)
ax.legend(handles=[patch_CT,patch_DE,patch_MA,patch_NJ,patch_NY,patch_PA,patch_RI,patch_VA], bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
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
plt.legend(labels=["Legend_Day1","Legend_Day2"], loc = 2, bbox_to_anchor = (0.85,1))

plt.show()

