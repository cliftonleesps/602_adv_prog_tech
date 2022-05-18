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
df = pd.read_csv("https://raw.githubusercontent.com/cliftonleesps/602_adv_prog_tech/main/final_project/Most-Recent-Cohorts-Institution_2.csv")

# show the data type
df.info()

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



# filter out rows where the median earnings are NaN
jdf = jdf[jdf['EARN_NE_MDN_3YR'].isna() == False]

# convert to float
jdf = jdf[jdf['EARN_NE_MDN_3YR'].isna() == False]
jdf['EARN_NE_MDN_3YR'] = jdf['EARN_NE_MDN_3YR'].astype(float)



#print(jdf.sort_values(ascending=False,by='EARN_MDN_HI_2YR')[['EARN_MDN_HI_2YR', 'INSTNM']].head(20))
#print(jdf.sort_values(ascending=False,by='EARN_NE_MDN_3YR')[['EARN_NE_MDN_3YR', 'HI_INC_DEBT_MDN', 'NPT4_PUB', 'TUITIONFEE_IN', 'ROOMBOARD_ON', 'INSTNM']].head(20))
print(jdf.sort_values(ascending=False,by='EARN_NE_MDN_3YR')[['EARN_NE_MDN_3YR', 'HI_INC_DEBT_MDN', 'NPT4_PUB','INSTNM']].head(20))





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




