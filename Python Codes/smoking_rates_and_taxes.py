import os
import numpy as np
import operator
import pandas as pd
import matplotlib.pyplot as plt
import taxes

def df_to_tuple_list(df, sort_key_num=0):
    """
    this function takes a dataframe as input and returns a sorted list of tuples
    intended to be used with year or other x-axis value as the first column and any other columns to follow
    originally used with dataframes with only 2 columns. not how three or more columns would work with plotting
    maybe columns after 2nd could be multiple y-values to plot vs x-axis values
    simple ascending sort by year is intended use
    :param df:
    :param sort_key_num: number of item within the tuple to use to order list
    :return: an ordered list of tuple in which the sort_key_num decides on which field to use for sorting items in list
    """
    tuple_list = sorted(df.items(), key=operator.itemgetter(sort_key_num))
    return tuple_list


def compare(set1, set2, title, legend_loc='lower left'):
    x1_values = []
    y1_values = []
    for x, y in set1['data']:
        x1_values.append(x)
        y1_values.append(y)

    x2_values = []
    y2_values = []
    for x, y in set2['data']:
        x2_values.append(x)
        y2_values.append(y)

    # fig, ax1 = plt.subplots()

    plt.figure()
    plt.plot(x1_values, y1_values, linestyle='-', marker='.', color='b')
    plt.plot(x2_values, y2_values, linestyle='-', marker='.', color='g')
    plt.xlabel(set1['xlabel'])
    plt.ylabel(set1['xlabel'])
    plt.title(title)
    plt.legend([set1['desc'], set2['desc']], loc=legend_loc)

    plt.draw_all()
    # plt.show()


def get_state_taxes(df1, state):
    """
    this function takes a dataframe and state name as input parameters and returns a dataframe containing only the data
    related to that state. There is no check for a valid state name.
    :param df1: dataframe containing data from all or several states
    :param state: name of state to be extracted and returned from df1
    :return: dataframe containing rows containing state of name passed in
    """
    # print("entering get_state: {}".format(state))
    # print("starting dataframe size: {}".format(df1.shape))
    df2 = df1[df1['STATE'] == state]
    # print(df2)
    # print("resulting dataframe size: {}".format(df2.shape))
    return df2


def get_year_taxes(df1, year):
    """
    this function takes a dataframe and year as input parameters and returns a dataframe containing only the data
    from that year. There is no check for a valid year.
    :param df1: dataframe containing data from all or several states
    :param state: yea of data to be extracted and returned from df1
    :return: dataframe containing rows containing data from year secified by caller
    """
    # print("entering get_year")
    # print("starting dataframe size: {}".format(df1.shape))
    df2 = df1[df1['YEAR'] == year]
    # print("resulting dataframe size: {}".format(df2.shape))
    return df2



def get_state(df1, state):
    """
    this function takes a dataframe and state name as input parameters and returns a dataframe containing only the data
    related to that state. There is no check for a valid state name.
    :param df1: dataframe containing data from all or several states
    :param state: name of state to be extracted and returned from df1
    :return: dataframe containing rows containing state of name passed in
    """
    # print("entering get_state: {}".format(state))
    # print("starting dataframe size: {}".format(df1.shape))
    df2 = df1[df1['LocationDesc'] == state]
    # print(df2)
    # print("resulting dataframe size: {}".format(df2.shape))
    return df2


def get_year(df1, year):
    """
    this function takes a dataframe and year as input parameters and returns a dataframe containing only the data
    from that year. There is no check for a valid year.
    :param df1: dataframe containing data from all or several states
    :param state: yea of data to be extracted and returned from df1
    :return: dataframe containing rows containing data from year secified by caller
    """
    # print("entering get_year")
    # print("starting dataframe size: {}".format(df1.shape))
    df2 = df1[df1['YEAR'] == year]
    # print("resulting dataframe size: {}".format(df2.shape))
    return df2


# survey_file_dir = "C:\\Users\\santoa39\\PycharmProjects\\survey2"
survey_file_dir = "C:\\Python for Data Science\\Assignments\\survey"
survey_file_name = "Youth_Tobacco_Survey__YTS__Data.csv"
# taxes_file_dir = "C:\\Users\\santoa39\\PycharmProjects\\survey2"
taxes_file_dir = "C:\\Python for Data Science\\Assignments\\survey"
taxes_file_name = "tax_data_all_cleaned.csv"

# output_file_dir = "C:\\Users\\santoa39\\PycharmProjects\\survey2"
output_file_dir = "C:\\Python for Data Science\\Assignments\\survey"
output_file_name = "YTS_data_cleaned.csv"

survey_data = pd.read_csv(os.path.join(survey_file_dir, survey_file_name))
survey_data = survey_data.replace(np.nan, ' ', regex=True)

# drop rows that have suppressed data
survey_data = survey_data[survey_data["Data_Value_Footnote"] != "Data in these cells have been suppressed because of a small sample size"]

# read taxes data into dataframe
taxes_df = pd.read_csv(os.path.join(taxes_file_dir, taxes_file_name))

# identify high-tax and low-tax states

# high_tax_states = ['Connecticut', 'Washington', 'New Jersey', 'New York', 'Rhode Island']
# low_tax_states = ['Missouri', 'Virginia', 'South Carolina', 'North Carolina', 'Georgia']
high_tax_states = taxes.get_high_tax_states(taxes_df, 6)
low_tax_states = taxes.get_low_tax_states(taxes_df, 6)

# create indexes for tobacco survey dataframe
cigarette_use = survey_data['TopicDesc'] == 'Cigarette Use (Youth)'
male_resp = survey_data['Gender']== 'Male'
female_resp = survey_data['Gender'] == 'Female'
current_use = survey_data['Response'] == 'Current'
high_school = survey_data['Education'] == 'High School'
middle_school = survey_data['Education'] == 'Middle School'
new_jersey = survey_data["LocationDesc"] == 'New Jersey'
nj_taxes = taxes_df["STATE"] == 'New Jersey'
high_tax_rates = survey_data["LocationDesc"].isin(high_tax_states)
low_tax_rates = survey_data["LocationDesc"].isin(low_tax_states)

# combine indexes via bitwise 'and'
# cig_male_hs_curr = cigarette_use & high_school & current_use & male_resp & high_tax_rates
cig_male_hs_curr = cigarette_use & high_school & current_use & male_resp
cig_male_hs_curr_hi_tax = cigarette_use & high_school & current_use & male_resp & high_tax_rates
cig_male_hs_curr_lo_tax = cigarette_use & high_school & current_use & male_resp & low_tax_rates

cig_female_hs_curr = cigarette_use & high_school & current_use & female_resp
cig_female_hs_curr_hi_tax = cigarette_use & high_school & current_use & female_resp & high_tax_rates
cig_female_hs_curr_lo_tax = cigarette_use & high_school & current_use & female_resp & low_tax_rates

# subset data of interest by copying columns of interest to new dataframe
columns_wanted = ['LocationDesc', 'Education', 'Gender', 'YEAR', 'TopicDesc', 'Data_Value']
limited_data = pd.DataFrame()
for col in columns_wanted:
    limited_data[col] = survey_data[col]

# calculate average rates by state
# create list of states
state_list = limited_data["LocationDesc"].unique()

states = {}
male_mean_rates = {}
for state in state_list:
    states[state] = get_state(limited_data[cig_male_hs_curr], state)
    if len(states[state].index) > 1:    # only include states with multiple data points
        mean_rate = states[state]["Data_Value"].mean()
        male_mean_rates[state] = mean_rate

# sort by smoking rate
sorted_rates_male = df_to_tuple_list(male_mean_rates, 1)

states = {}
female_mean_rates = {}
for state in state_list:
    states[state] = get_state(limited_data[cig_female_hs_curr], state)
    if len(states[state].index) > 1:    # only include states with multiple data points
        mean_rate = states[state]["Data_Value"].mean()
        female_mean_rates[state] = mean_rate

# sort by smoking rate
sorted_rates_female = df_to_tuple_list(male_mean_rates, 1)

# not currently using these variables
# get 5 lowest average rates
bottom5_states_male = [state for state, _ in sorted_rates_male[0:5]]
# get 5 highest average rates
top5_states_male = [state for state, _ in sorted_rates_male[-5:]]

# save survey data to csv file
survey_data.to_csv(os.path.join(output_file_dir, output_file_name), index=False)

# plot smoking rates for top 5 average tax rate states
rates_high_taxes = {}
rate_ix = 0
for index, row in limited_data[cig_male_hs_curr_hi_tax].iterrows():
    rates_high_taxes[row["YEAR"]] = row["Data_Value"]
    rate_ix += 1

# plot smoking rates for bottom 5 average tax rate states
rates_low_taxes = {}
rate_ix = 0
for index, row in limited_data[cig_male_hs_curr_lo_tax].iterrows():
    rates_low_taxes[row["YEAR"]] = row["Data_Value"]
    rate_ix += 1

# calculate mean tax rate high tax states


# order smoking rates by year and then place into list of tuples
ordered_rates_high = df_to_tuple_list(rates_high_taxes, 0)
# print(ordered_rates_high)
x1_values = []
y1_values = []
for x, y in ordered_rates_high:
    x1_values.append(x)
    y1_values.append(y)

# order smoking rates by year and then place into list of tuples
ordered_rates_low = df_to_tuple_list(rates_low_taxes, 0)
# print(ordered_rates_low)
x2_values = []
y2_values = []
for x, y in ordered_rates_low:
    x2_values.append(x)
    y2_values.append(y)

# prepare data for comparison/plotting
ds1 = {}
ds2 = {}
ds1['data'] = ordered_rates_high
ds1['xlabel'] = 'Year'
ds1['ylabel'] = 'Smoking Rate'
ds1['desc'] = 'High Tax States'

ds2['data'] = ordered_rates_low
ds2['xlabel'] = 'Year'
ds2['ylabel'] = 'Smoking Rate'
ds2['desc'] = 'Low Tax States'
compare(ds1, ds2, title='Smoking Rate (Males) - High Tax & Low Tax States')

# compare tax rates over time between high-tax and low-tax states
# get lowest average rates
bottom_states = taxes.get_low_tax_states(taxes_df, 10)
bottom_states_rates = taxes.get_average_rate_by_year(taxes_df, bottom_states)

# sort taxes by year to get list of tuples
ordered_states_low = df_to_tuple_list(bottom_states_rates)

# get highest average rates
top_states = taxes.get_high_tax_states(taxes_df, 10)
top_states_rates = taxes.get_average_rate_by_year(taxes_df, top_states)

# sort taxes by year to get list of tuples
ordered_states_high = df_to_tuple_list(top_states_rates, sort_key_num=0)

# prepare tax data for comparison/plotting
ds1 = {}
ds2 = {}
ds1['data'] = ordered_states_high
ds1['xlabel'] = 'Year'
ds1['ylabel'] = 'Per-pack taxes'
ds1['desc'] = 'High Tax States'

ds2['data'] = ordered_states_low
ds2['xlabel'] = 'Year'
ds2['ylabel'] = 'Per-pack Taxes'
ds2['desc'] = 'Low Tax States'
compare(ds1, ds2, title='Per-pack taxes - High Tax & Low Tax States', legend_loc='upper left')

plt.show()