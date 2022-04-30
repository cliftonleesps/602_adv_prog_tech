import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def filter_non_numeric(dataframe, convert_columns):
    for c in convert_columns:
        dataframe = dataframe[dataframe[c] != 'PrivacySuppressed']
        dataframe = dataframe[dataframe[c] != 'NULL']
        dataframe = dataframe[dataframe[c] != 'E00602']
        dataframe = dataframe[dataframe[c] != 'G02485']
        dataframe[c] = pd.to_numeric(dataframe[c])
    return dataframe


connection = sqlalchemy.create_engine('mysql+pymysql://ddd:rrrr@localhost:3306/college')

sql_states="select count(*) as Count, STABBR as State from file1 join file4 on file1.UNITID = file4.UNITID where STABBR in ('NY', 'PA','DE','VA','NJ','CT','RI','MA') AND SCHTYPE = 1 and ACCREDAGENCY not in ('NULL', 'EXEMPT') group by STABBR"



df = pd.read_sql(sql_states, connection)
print(df)
# now make a barchart
sns.barplot(data=df,x="State", y="Count", palette="deep")

plt.show()


# mean tuition
sql_mean_tuition="select NPT4_PUB as tuition from file1 join file4 on file1.UNITID = file4.UNITID where STABBR in ('NY', 'PA','DE','VA','NJ','CT','RI','MA') AND SCHTYPE = 1 and ACCREDAGENCY not in ('NULL', 'EXEMPT')"
df_tuition = pd.read_sql(sql_mean_tuition, connection)
df_tuition = df_tuition[df_tuition['tuition'] != 'NULL']
df_tuition['tuition'] = pd.to_numeric(df_tuition['tuition'])

#print(df_tuition['tuition'])
#print(df_tuition.describe())

sns.histplot(data=df_tuition, x="tuition")


# Use the merge function to join two dataframes
sql_file1 = 'select UNITID, OPEID, INSTNM, STABBR, NPT4_PUB from file1 limit 300'
sql_file2 = 'select UNITID, OPEID, NOLOAN_YR8_N from file4 limit 300'
sql_file4 = 'select UNITID, SCHTYPE from file4 limit 300'

df1 = pd.read_sql(sql_file1, connection)
df2 = pd.read_sql(sql_file2, connection)
df4 = pd.read_sql(sql_file4, connection)
print(df1)
print(df2)


df_merged = pd.merge(df1,
                     df2,
                     left_on='UNITID',
                     right_on='UNITID',
                     how='inner')
df_merged = pd.merge(df_merged,
                     df4,
                     left_on='UNITID',
                     right_on='UNITID',
                     how='inner')
df_merged= df_merged.drop(columns=['OPEID_x', 'OPEID_y'])
print(df_merged)




print(df)


columns = ['AVGFACSAL', 'TUITIONFEE_IN','TUITIONFEE_OUT', 'NPT4_PUB']



# for
df_tuition = pd.read_sql('select AVGFACSAL, TUITIONFEE_IN,TUITIONFEE_OUT, NPT4_PUB, STABBR from file1 where CONTROL = 1 and STABBR in ("NY", "PA","DE","VA","NJ","CT","RI","MA") ', connection)
print(df_tuition)


df_tuition = filter_non_numeric(df_tuition, columns)


# Scatterplot
# remove NULLs
df_tuition = df_tuition[df_tuition['NPT4_PUB'] != 'NULL']
df_tuition = df_tuition[df_tuition['TUITIONFEE_IN'] != 'NULL']
df_tuition = df_tuition[df_tuition['TUITIONFEE_OUT'] != 'NULL']
df_tuition = df_tuition[df_tuition['AVGFACSAL'] != 'NULL']

df_tuition['NPT4_PUB'] = pd.to_numeric(df_tuition['NPT4_PUB'])
df_tuition['TUITIONFEE_IN'] = pd.to_numeric(df_tuition['TUITIONFEE_IN'])
df_tuition['TUITIONFEE_OUT'] = pd.to_numeric(df_tuition['TUITIONFEE_OUT'])
df_tuition['AVGFACSAL'] = pd.to_numeric(df_tuition['AVGFACSAL']) * 10
sns.scatterplot(data=df_tuition, x="AVGFACSAL", y="NPT4_PUB", hue="STABBR")
plt.show()
print(df_tuition)
# histogram
# with cleanup
df_earnings = pd.read_sql('select EARN_MDN_HI_2YR from cohort order by EARN_MDN_HI_2YR', connection)
df_earnings = df_earnings[df_earnings['EARN_MDN_HI_2YR'] != 'PrivacySuppressed']
df_earnings = df_earnings[df_earnings['EARN_MDN_HI_2YR'] != 'NULL']
df_earnings['EARN_MDN_HI_2YR'] = pd.to_numeric(df_earnings['EARN_MDN_HI_2YR'])
sns.histplot(data=df_earnings, x="EARN_MDN_HI_2YR")
plt.show()



# mean earnigs after college and not pursuing another degree
#select MN_EARN_WNE_P7, MN_EARN_WNE_P6, MN_EARN_WNE_P8, MN_EARN_WNE_P9, MN_EARN_WNE_P10 from file4 limit 50;

# repayment progress after X years
#select NONCOM_RPY_1YR_RT, COMPL_RPY_1YR_RT, COMPL_RPY_3YR_RT, NONCOM_RPY_3YR_RT,COMPL_RPY_5YR_RT, COMPL_RPY_7YR_RT from file3 limit 10; 


# Recreate https://college-insight.org/topics/cost-of-attendance/2
# select a.UNITID, CONTROL, TUITIONFEE_IN, BOOKSUPPLY, ROOMBOARD_ON, OTHEREXPENSE_ON  from file1 as a join file5 as b on a.UNITID = b.UNITID join file4 as c on a.UNITID = c.UNITID limit 10;
sql_cost = 'select a.UNITID, CONTROL, TUITIONFEE_IN, BOOKSUPPLY, ROOMBOARD_ON, OTHEREXPENSE_ON  from file1 as a join file5 as b on a.UNITID = b.UNITID join file4 as c on a.UNITID = c.UNITID where SCH_DEG = 3 limit 1000';

df_cost = pd.read_sql(sql_cost, connection)



columns = ['TUITIONFEE_IN', 'BOOKSUPPLY', 'ROOMBOARD_ON', 'OTHEREXPENSE_ON', 'CONTROL']

df_cost = pd.read_sql(sql_cost, connection)
df_cost = filter_non_numeric(df_cost, columns)
df_control1 = df_cost[df_cost['CONTROL'] == 1 ]
df_control2 = df_cost[df_cost['CONTROL'] == 2]
df_control3 = df_cost[df_cost['CONTROL'] == 3]


# make a new chart dataframe
df_cost_chart = pd.DataFrame( { 'Tuition (In State)' : [df_control1['TUITIONFEE_IN'].median(), df_control2['TUITIONFEE_IN'].median(), df_control3['TUITIONFEE_IN'].median()],
                                'Book' : [df_control1['BOOKSUPPLY'].median(), df_control2['BOOKSUPPLY'].median(), df_control3['BOOKSUPPLY'].median()],
                                'Dorm' : [df_control1['ROOMBOARD_ON'].median(), df_control2['ROOMBOARD_ON'].median(), df_control3['ROOMBOARD_ON'].median()],
                                'Other' : [df_control1['OTHEREXPENSE_ON'].median(), df_control2['OTHEREXPENSE_ON'].median(), df_control3['OTHEREXPENSE_ON'].median()]},
                              index = ['Public','Private nonprofit','Private for-profit'])
 



df_cost_chart.plot(kind='bar', stacked=True, color=['orange', 'skyblue', 'green', 'gray'])
plt.xticks(rotation=0)
plt.title('Median Costs of College')
plt.xlabel('College Type')
plt.show()

sns.barplot(data=df_cost_chart, x=['Public','Private nonprofit','Private for-profit'], y="Tuition (In State)", color='darksalmon')
sns.barplot(data=df_cost_chart, x=['Public','Private nonprofit','Private for-profit'], y="Dorm", color='lightgrey')
sns.barplot(data=df_cost_chart, x=['Public','Private nonprofit','Private for-profit'], y="Other", color='darkblue')
sns.barplot(data=df_cost_chart, x=['Public','Private nonprofit','Private for-profit'], y="Book", color='lightblue')

plt.show()




sql_cost_vs_debt = 'select a.UNITID, STABBR, CONTROL, TUITIONFEE_IN + BOOKSUPPLY +ROOMBOARD_ON + OTHEREXPENSE_ON as total_cost, DEP_DEBT_MDN, CUML_DEBT_N  from file1 as a join file5 as b on a.UNITID = b.UNITID join file4 as c on a.UNITID = c.UNITID where SCH_DEG = 3';
df_cost_vs_debt = pd.read_sql(sql_cost_vs_debt, connection)

df_cost_vs_debt = filter_non_numeric(df_cost_vs_debt, ['total_cost','DEP_DEBT_MDN', 'CUML_DEBT_N'])
df_cost_vs_debt = df_cost_vs_debt[df_cost_vs_debt['total_cost'] < 200000]

sns.scatterplot(data=df_cost_vs_debt, x="total_cost", y="DEP_DEBT_MDN", size="CUML_DEBT_N", sizes=(20, 200), legend=False, hue="STABBR")
plt.show()
