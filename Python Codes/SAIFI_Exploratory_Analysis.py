import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Read the csv into a df
dfMAIN = pd.read_csv('YTS_Clean.csv')

# Set conditions to use to sort/select data
post_tips = dfMAIN['YEAR'] >= 2012
pre_tips = dfMAIN['YEAR'] < 2012

smoking_status = dfMAIN['MeasureDesc'] == 'Smoking Status'

cigg_use = dfMAIN['TopicDesc'] == 'Cigarette Use (Youth)'
smokeless = dfMAIN['TopicDesc'] == 'Smokeless Tobacco Use (Youth)'

gender_male = dfMAIN['Gender'] == 'Male'
gender_female = dfMAIN['Gender'] == 'Female'
gender_overall = dfMAIN['Gender'] == 'Overall'

current_user = dfMAIN['Response'] == 'Current'
ever_user = dfMAIN['Response'] == 'Ever'
frequent_user = dfMAIN['Response'] == 'Frequent'

high_school = dfMAIN['Education'] == 'High School'
middle_school = dfMAIN['Education'] == 'Middle School'


# Overall Cigeratte Use (Current) Boxplot Pre TIPS Campaign

df_CigUse_PreTIPS = dfMAIN[cigg_use & smoking_status & current_user & pre_tips & gender_overall]
plot_CigUse_PreTIPS = df_CigUse_PreTIPS.Data_Value.plot.box(title = 'Overall Cigeratte Use (Current) Pre TIPS Campaign', label = '%age',figsize = (15,15))
plt.savefig('cig_use_preTIPS.png')
plt.clf()

# Overall Cigeratte Use (Current) Boxplot POST TIPS Campaign

df_CigUse_PostTIPS = dfMAIN[cigg_use & smoking_status & current_user & post_tips & gender_overall]
plot_CigUse_PostTIPS = df_CigUse_PreTIPS.Data_Value.plot(kind='box', title = 'Overall Cigeratte Use (Current) POST TIPS Campaign', label = '%age',figsize = (15,15))
plt.savefig('cig_use_POSTTIPS.png')
plt.clf()

# Overall Cigeratte Use (Current) Boxplot by Gender

df_CigUse_Overall = dfMAIN[cigg_use & smoking_status & current_user]
df_CigUse_Overall.boxplot(column='Data_Value',by='Gender', figsize=(15,15))
plt.savefig('cig_use_by_Gender.png', title='Cig Use by Gender',label='%age')
plt.clf()


# Smokeless Tobacco Declines As Well..

df_smokeless = dfMAIN[smokeless][['YEAR', 'LocationAbbr','Data_Value']]
df_smokeless = df_smokeless.groupby(by='YEAR').mean()
df_smokeless.plot.line(figsize=(15,15), title='Smokeless Tobacco Declines in Popularity', legend=False)
plt.savefig('fall_in_smokeless.png')
plt.clf()





