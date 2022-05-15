import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.ticker as tkr
import matplotlib.patches as mpatches
from matplotlib.axis import Axis


#df = pd.read_csv("https://raw.githubusercontent.com/cliftonleesps/602_adv_prog_tech/main/final_project/df_out.csv")
df = pd.read_csv("df_out_2.csv")

# show the data type
#df.info()

# subset for nearby, public colleges
df = df[df['ACCREDAGENCY'].isnull() == False]
df = df[df['CONTROL'] == 1]  # public
df = df[df['SCH_DEG'] == 3]  # bachelor's primary degree type awarded
df = df[df['STABBR'].isin(['NY', 'PA','DE','VA','NJ','CT','RI','MA'])]
df = df.replace('PrivacySuppressed', np.nan)  # replace all privacy suppressed values
df['GRAD_DEBT_MDN'] = pd.to_numeric(df['GRAD_DEBT_MDN'])
df['CUML_DEBT_N'] = pd.to_numeric(df['CUML_DEBT_N'])


fields = pd.read_csv("Most-Recent-Cohorts-Field-of-Study.csv")
fields = fields.replace('PrivacySuppressed', np.nan)
fields['EARN_MDN_HI_1YR'] = pd.to_numeric(fields['EARN_MDN_HI_1YR'])
fields['EARN_MDN_HI_2YR'] = pd.to_numeric(fields['EARN_MDN_HI_2YR'])
fields['EARN_NE_MDN_3YR'] = pd.to_numeric(fields['EARN_NE_MDN_3YR'])

# filter for CS major and bachelor's
fields = fields[(fields['CIPCODE'] == 1101) & (fields['CREDLEV'] == 3)]
fields = fields[fields['CONTROL'] == 'Public']



jdf = df.join(fields.set_index('UNITID'), on='UNITID', rsuffix = "_fields")


#print(jdf.sort_values(ascending=False,by='EARN_MDN_HI_2YR')[['EARN_MDN_HI_2YR', 'INSTNM']].head(20))
#print(jdf.sort_values(ascending=False,by='EARN_NE_MDN_3YR')[['EARN_NE_MDN_3YR', 'HI_INC_DEBT_MDN', 'NPT4_PUB', 'TUITIONFEE_IN', 'ROOMBOARD_ON', 'INSTNM']].head(20))
print(jdf.sort_values(ascending=False,by='EARN_NE_MDN_3YR')[['EARN_NE_MDN_3YR', 'HI_INC_DEBT_MDN', 'NPT4_PUB','INSTNM']].head(20))




color_map = {
'CT' : '#16697a',
 'DE' : '#489fb5',
 'MA' : '#82c0cc',
 'NJ' : '#fe6d73',
 'NY' : '#ffa62b',
 'PA' : '#353535',
 'RI' : '#aec3b0',
 'VA' : '#a98467'
}
color_array = []

# make a color array mapped to each state
for s in jdf['STABBR']:
  color_array.append(color_map[s])

fig = go.Figure(data=go.Scatter(x=jdf['EARN_NE_MDN_3YR'],y=jdf['HI_INC_DEBT_MDN'], mode='markers', marker_color=color_array,text=jdf['INSTNM']))
fig.update_traces(marker=dict(size=12))
fig.update_layout(title='Median Annual Earnings Versus Median Debt')
fig.show()



