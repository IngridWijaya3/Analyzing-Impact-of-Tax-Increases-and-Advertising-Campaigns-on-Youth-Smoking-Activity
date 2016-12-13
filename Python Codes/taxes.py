"""
this library contains functions to work with the tax rate data
it provides functionality to retrieve states with the highest taxes and states with the lowest taxes
"""
import csv
import pandas as pd
import operator



def get_state(df1, state):
    """
    this function takes a dataframe and state name as input parameters and returns a dataframe containing only the data
    related to that state. There is no check for a valid state name.
    :param df1: dataframe containing data from all or several states
    :param state: name of state to be extracted and returned from df1
    :return: dataframe containing rows containing state of name passed in
    """
    state_ix = df1['STATE'] == state
    df2 = df1[state_ix]
    return df2


def get_year(df1, year):
    """
    this function takes a dataframe and year as input parameters and returns a dataframe containing only the data
    from that year. There is no check for a valid year.
    :param df1: dataframe containing data from all or several states
    :param state: yea of data to be extracted and returned from df1
    :return: dataframe containing rows containing data from year secified by caller
    """
    df2 = df1[df1['YEAR'] == year]
    return df2


def get_high_tax_states(df, num_states=5):
    ordered_taxes_by_year = {}
    top5 = {}
    bottom5 = {}
    for year in range(2000, 2015):
        ordered_taxes_by_year[year] = get_year(df, year).sort_values(by="TAX RATE", ascending=False, inplace=False)
        # top5[year] = ordered_taxes_by_year[year][:5]
        # bottom5[year] = ordered_taxes_by_year[year][-5:]

    state_list = df["STATE"].unique()
    states = {}
    mean_rates = {}
    for state in state_list:
        states[state] = get_state(df, state)
        mean_rate = states[state]["TAX RATE"].mean()
        mean_rates[state] = mean_rate

    sorted_rates = sorted(mean_rates.items(), key=operator.itemgetter(1))
    # print(sorted_rates)
    # get 5 highest average rates
    top_states = [state for state, rate in sorted_rates[-(num_states):]] # get last n states
    return top_states

def get_low_tax_states(df, num_states=5):
    ordered_taxes_by_year = {}
    top5 = {}
    bottom5 = {}
    for year in range(2000, 2015):
        ordered_taxes_by_year[year] = get_year(df, year).sort_values(by="TAX RATE", ascending=False, inplace=False)
        # top5[year] = ordered_taxes_by_year[year][:5]
        # bottom5[year] = ordered_taxes_by_year[year][-5:]

    state_list = df["STATE"].unique()
    states = {}
    mean_rates = {}
    for state in state_list:
        states[state] = get_state(df, state)
        mean_rate = states[state]["TAX RATE"].mean()
        mean_rates[state] = mean_rate

    sorted_rates = sorted(mean_rates.items(), key=operator.itemgetter(1))
    # print(sorted_rates)
    # get 5 highest average rates
    bottom_states = [state for state, rate in sorted_rates[0:num_states]] #  get 1st n states
    return bottom_states

def get_average_rate(df, state_list):
    state_rows = df["STATE"].isin(state_list)
    mean_rate = df[state_rows]["TAX RATE"].mean()
    return mean_rate

def get_average_rate_by_year(df, state_list):
    year_list = df["YEAR"].unique()
    mean_rates = {}
    for year in year_list:
        state_rows = df["STATE"].isin(state_list)
        year_rows = df["YEAR"] == year
        mean_rates[year] = df[state_rows & year_rows]["TAX RATE"].mean()
    return mean_rates


def main():
    # df1 = pd.read_csv("C:\\Users\\santoa39\\PycharmProjects\\survey\\tax_data_all.csv")
    df1 = pd.read_csv("C:\\Python for Data Science\\Assignments\\survey\\tax_data_all_cleaned.csv")

    states = df1['STATE'].unique()

    highest_tax = max(df1[df1['YEAR'] == 2014]['TAX RATE'])
    print("highest tax: {}".format(highest_tax))

    # get 5 lowest average rates
    bottom_states = get_low_tax_states(df1, 10)
    # get 5 highest average rates
    top_states = get_high_tax_states(df1, 10)
    # bottom5_states = sorted_rates[0:5]
    # top5_states = sorted_rates[-5:]
    print("\nstates with lowest average cigarette taxes from 2000 - 2014:")
    print(bottom_states)
    print("states with highest average cigarette taxes from 2000 - 2014:")
    print(top_states)
    print("bottom: ", get_average_rate(df1, bottom_states))
    print("average of high tax states: ", get_average_rate(df1, top_states))
    print("average of high tax states by year: ", get_average_rate_by_year(df1, top_states))
    print("average of high low states by year: ", get_average_rate_by_year(df1, bottom_states))


    # print(state_list)
if __name__ == '__main__':
    main()