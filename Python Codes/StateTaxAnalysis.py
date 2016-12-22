import math
import pandas as pd
import operator
import matplotlib.pyplot as plt
import os
import taxes
from YouthSmokingAnalysis import YouthSmokingAnalysis
"""
This program performs an analysis of the effect of tax increases smoking rates, cessation rates, and whether there is a
correlation between the size of the tax increase and the amount smoking rates decrease.
Author: Tony Santos, Group 4
"""

class DataSet:
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values
        self.title = ''
        self.xlabel = ''
        self.ylabel = ''

    def set_title(self, title_text):
        self.title = title_text

    def get_title(self):
        return self.title

    def set_xlabel(self, xlabel_text):
        self.xlabel = xlabel_text

    def set_ylabel(self, ylabel_text):
        self.ylabel = ylabel_text

    def get_xvalues(self):
        return self.x_values

    def get_yvalues(self):
        return self.y_values

    def get_xlabel(self):
        return self.xlabel

    def get_ylabel(self):
        return self.ylabel

    def set_filename(self, filename):
        self.filename = filename

    def get_filename(self):
        return self.filename


class StateAnalysis(YouthSmokingAnalysis):
    def __init__(self):
        YouthSmokingAnalysis.__init__(self)
        self.high_tax_states = taxes.get_high_tax_states(self.taxRateDataFrame, 6)
        self.low_tax_states = taxes.get_low_tax_states(self.taxRateDataFrame, 6)

        # create list of states
        self.state_list = self.taxRateDataFrame["STATE"].unique()


    def analyze(self):

        self.analyzeCigaretteUse()
        self.analyzeCessation()
        self.analyzeBeforeAndAfterTax()

    def get_state(self, df1, state):
        """
        this method takes a dataframe and state name as input parameters and returns a dataframe containing only the data
        related to that state. There is no check for a valid state name.
        :param df1: dataframe containing data from all or several states
        :param state: name of state to be extracted and returned from df1
        :return: dataframe containing rows containing state of name passed in
        """
        df2 = df1[df1['LocationDesc'] == state]
        return df2

    def tuple_list_to_csv(self, tuple_list, column_list, filename):
        # outputPlotFolderName = "Plots"
        with open(os.path.join(YouthSmokingAnalysis.outputCSVFolderName, filename), "w") as outfile:
            outfile.write("YEAR,% CURRENT SMOKERS WHO WANT TO QUIT\n")
            for x, y in tuple_list:
                outfile.write("{},{}\n".format(x, y))

    def df_to_tuple_list(self, df, sort_key_num=0):
        """
        this method takes a dataframe as input and returns a sorted list of tuples
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

    def analyzeCessation(self):
        cessation_topic = self.ytsDataFrame['TopicDesc'] == 'Cessation (Youth)'
        cessation_question = self.ytsDataFrame['MeasureDesc'] == 'Percent of Current Smokers Who Want to Quit'
        male_resp = self.ytsDataFrame['Gender'] == 'Male'
        female_resp = self.ytsDataFrame['Gender'] == 'Female'
        high_school = self.ytsDataFrame['Education'] == 'High School'

        high_tax_rates = self.ytsDataFrame["LocationDesc"].isin(self.high_tax_states)
        low_tax_rates = self.ytsDataFrame["LocationDesc"].isin(self.low_tax_states)

        cess_hs_male = cessation_topic & cessation_question & high_school & male_resp
        cess_hs_hi_tax_male = cessation_topic & cessation_question & high_school & high_tax_rates & male_resp
        cess_hs_lo_tax_male = cessation_topic & cessation_question & high_school & low_tax_rates & male_resp

        # subset data of interest by copying columns of interest to new dataframe
        columns_wanted = ['LocationDesc', 'Education', 'Gender', 'YEAR', 'TopicDesc', 'Data_Value']
        limited_data = pd.DataFrame()
        limited_data = self.ytsDataFrame[columns_wanted]

        # get smoking rates for top 5 average tax rate states
        rates_high_taxes = {}
        rate_ix = 0
        for index, row in limited_data[cess_hs_hi_tax_male].iterrows():
            rates_high_taxes[row["YEAR"]] = row["Data_Value"]
            rate_ix += 1

        # get cessation rates for bottom 5 average tax rate states
        rates_low_taxes = {}
        rate_ix = 0
        for index, row in limited_data[cess_hs_lo_tax_male].iterrows():
            rates_low_taxes[row["YEAR"]] = row["Data_Value"]
            rate_ix += 1

        # order cessation rates by year and then place into list of tuples
        ordered_rates_high = self.df_to_tuple_list(rates_high_taxes, 0)
        self.tuple_list_to_csv(ordered_rates_high, column_list=["YEAR", "PERCENT CURRENT SMOKERS WHO WANT TO QUIT"],
                               filename="cessation_rates_high_tax_states.csv")

        # convert tuples into list of x-values and y-values for plotting
        x1_values = []
        y1_values = []
        for x, y in ordered_rates_high:
            x1_values.append(x)
            y1_values.append(y)

        # order smoking rates by year and then place into list of tuples
        ordered_rates_low = self.df_to_tuple_list(rates_low_taxes, 0)
        self.tuple_list_to_csv(ordered_rates_low, column_list=["YEAR", "PERCENT CURRENT SMOKERS WHO WANT TO QUIT"],
                               filename="cessation_rates_low_tax_states.csv")

        # convert tuples into list of x-values and y-values for plotting
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
        ds1['ylabel'] = '% Smokers That Want To Quit'
        ds1['desc'] = 'High Tax States'

        ds2['data'] = ordered_rates_low
        ds2['xlabel'] = 'Year'
        ds2['ylabel'] = '% Smokers That Want To Quit'
        ds2['desc'] = 'Low Tax States'
        self.compare(ds1, ds2, title='Cessation Rate (High School Students) - High Tax & Low Tax States',
                     filename='cessation_low_tax_high_tax.png')

    def analyzeCigaretteUse(self):
        # create indexes for tobacco survey dataframe
        cigarette_use = self.ytsDataFrame['TopicDesc'] == 'Cigarette Use (Youth)'
        male_resp = self.ytsDataFrame['Gender'] == 'Male'
        female_resp = self.ytsDataFrame['Gender'] == 'Female'
        current_use = self.ytsDataFrame['Response'] == 'Current'
        high_school = self.ytsDataFrame['Education'] == 'High School'
        middle_school = self.ytsDataFrame['Education'] == 'Middle School'

        increases = self.get_increases()
        ordered_increases = self.df_to_tuple_list(increases, 1)

        high_tax_rates = self.ytsDataFrame["LocationDesc"].isin(self.high_tax_states)
        low_tax_rates = self.ytsDataFrame["LocationDesc"].isin(self.low_tax_states)

        cig_hs_curr = cigarette_use & high_school & current_use & male_resp
        cig_hs_curr_hi_tax = cigarette_use & high_school & current_use & high_tax_rates & male_resp
        cig_hs_curr_lo_tax = cigarette_use & high_school & current_use & low_tax_rates & male_resp

        # subset data of interest by copying columns of interest to new dataframe
        columns_wanted = ['LocationDesc', 'Education', 'Gender', 'YEAR', 'TopicDesc', 'Data_Value']
        limited_data = pd.DataFrame()
        limited_data = self.ytsDataFrame[columns_wanted]

        # get smoking rates for top 5 average tax rate states
        rates_high_taxes = {}
        rate_ix = 0
        for index, row in limited_data[cig_hs_curr_hi_tax].iterrows():
            rates_high_taxes[row["YEAR"]] = row["Data_Value"]
            rate_ix += 1

        # get smoking rates for bottom 5 average tax rate states
        rates_low_taxes = {}
        rate_ix = 0
        for index, row in limited_data[cig_hs_curr_lo_tax].iterrows():
            rates_low_taxes[row["YEAR"]] = row["Data_Value"]
            rate_ix += 1

        # order smoking rates by year and then place into list of tuples
        ordered_rates_high = self.df_to_tuple_list(rates_high_taxes, 0)
        self.tuple_list_to_csv(ordered_rates_high, column_list=["YEAR", "PERCENT RESPONDING AS CURRENT SMOKERS"],
                               filename="cigarette_use_rates_high_tax_states.csv")

        # convert tuples into list of x-values and y-values for plotting
        x1_values = []
        y1_values = []
        for x, y in ordered_rates_high:
            x1_values.append(x)
            y1_values.append(y)

        # order smoking rates by year and then place into list of tuples
        ordered_rates_low = self.df_to_tuple_list(rates_low_taxes, 0)
        self.tuple_list_to_csv(ordered_rates_low, column_list=["YEAR", "PERCENT RESPONDING AS CURRENT SMOKERS"],
                               filename="cigarette_use_rates_low_tax_states.csv")

        # convert tuples into list of x-values and y-values for plotting
        x2_values = []
        y2_values = []
        for x, y in ordered_rates_low:
            x2_values.append(x)
            y2_values.append(y)

        # get smoking rates by year for top 5 average tax rate states
        rates_high_taxes = {}
        rate_ix = 0
        for index, row in limited_data[cig_hs_curr_hi_tax].iterrows():
            rates_high_taxes[row["YEAR"]] = row["Data_Value"]
            rate_ix += 1

        # plot smoking rates by year for bottom 5 average tax rate states
        rates_low_taxes = {}
        rate_ix = 0
        for index, row in limited_data[cig_hs_curr_lo_tax].iterrows():
            rates_low_taxes[row["YEAR"]] = row["Data_Value"]
            rate_ix += 1

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

        self.compare(ds1, ds2, title='Smoking Rate (High School Students) - High Tax & Low Tax States',
                     filename='cig_use_high_tax_low_tax.png')

    def analyzeBeforeAndAfterTax(self):
        cigarette_use = self.ytsDataFrame['TopicDesc'] == 'Cigarette Use (Youth)'
        overall_resp = self.ytsDataFrame['Gender'] == 'Overall'
        male_resp = self.ytsDataFrame['Gender'] == 'Male'
        female_resp = self.ytsDataFrame['Gender'] == 'Female'
        current_use = self.ytsDataFrame['Response'] == 'Current'
        high_school = self.ytsDataFrame['Education'] == 'High School'
        middle_school = self.ytsDataFrame['Education'] == 'Middle School'

        cig_hs_curr = cigarette_use & high_school & current_use & overall_resp

        cig_hs_curr_data = self.ytsDataFrame[cig_hs_curr]
        # get list of largest tax increases by state
        max_increases = {}
        increase_effect_data = []
        for state in self.state_list:
            increases = []
            ix = 0
            max_increase = 0
            max_increase_year = 0
            state_tax_rates = self.taxRateDataFrame[self.taxRateDataFrame["STATE"] == state][["STATE", "YEAR", "TAX RATE"]]
            for year in range(2001, 2015):
                prior_year = year - 1
                curr_tax = state_tax_rates[state_tax_rates["YEAR"]==year]["TAX RATE"].min()
                prev_tax = state_tax_rates[state_tax_rates["YEAR"]==prior_year]["TAX RATE"].min()
                increase = curr_tax - prev_tax
                if increase > max_increase:
                    max_increase_year = year
                    max_increase = increase
            # store result in a dict where key is state name and value is a tuple of the largest increase and the year it occurred
            max_increases[state] = (max_increase, max_increase_year)

            # calculate cigarette use averages before and after the largest tax increase for the state
            before, after = self.calc_before_after_averages(cig_hs_curr_data, state, max_increase_year)
            if math.isnan(before) or math.isnan(after):
                pass        # only add valid data points to be plotted
            else:
                change = before - after
                increase_effect_data.append((max_increase, change))
        # sort increase effect data by size of tax increase - 1st element in tuple
        ordered_increases = sorted(increase_effect_data, key=lambda x: x[0])
        self.tuple_list_to_csv(ordered_increases, column_list=["TAX INCREASE", "DROP IN CURRENT SMOKER RATE"],
                               filename="current_smoker_rates_tax_increases.csv")


        # convert tuples into lists of x-values and y-values for plotting
        x1_values = []
        y1_values = []
        for x, y in ordered_increases:
            x1_values.append(x)
            y1_values.append(y)

        # plot average change by increase
        dataset = DataSet(x1_values, y1_values)
        dataset.set_xlabel('Tax increase in cents')
        dataset.set_ylabel('Decrease in smoking rate average')
        dataset.set_title('Change in smoking rates by tax increase')
        dataset.set_filename('cig_use_change_tax_increase.png')
        # plt.show()
        self.plotResult(dataset, filename='cig_use_change_tax_increase.png')

    def plotResult(self, dataset, filename):
        """
        this methos overrides the method in the superclass
        it takes a dataset object as input and uses matplotlib to produce a graph. it is used top plot a single set
        of data points
        :param dataset:
        :return: no return value
        """
        plt.figure()
        plt.style.use('fivethirtyeight')
        plt.plot(dataset.get_xvalues(), dataset.get_yvalues(), linestyle='-', marker='.', color='b')
        plt.xlabel(dataset.get_xlabel())
        plt.ylabel(dataset.get_ylabel())
        plt.title(dataset.get_title())

        plt.draw_all()

        savepath = YouthSmokingAnalysis.outputPlotFolderName + "/" + filename
        plt.savefig(savepath)

    def calc_before_after_averages(self, df, state, year):
        # since we don't know when in the year the increase went into effect, ignore year of increase
        avg_before = {}
        # lis of years before year of largest tax increase
        before_years = [yr for yr in range(2000, year)]
        # list of years after year of largest tax increase
        after_years = [yr for yr in range(year+1, 2014)]

        # indexes
        state_data = df["LocationDesc"] == state
        before_data = df["YEAR"].isin(before_years)
        after_data = df["YEAR"].isin(after_years)

        # calculate average of smoking rates of state for years prior-to and after largest tax increase
        before_average = df[state_data & before_data]["Data_Value"].mean()
        after_average = df[state_data & after_data]["Data_Value"].mean()

        return(before_average, after_average)

    def compare(self, set1, set2, title, filename, legend_loc='lower left'):
        """
        This method is used to plot two sets of data on the same graph
        :param set1:
        :param set2:
        :param title:
        :param filename:
        :param legend_loc:
        :return:
        """
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
        plt.style.use('fivethirtyeight')
        plt.plot(x1_values, y1_values, linestyle='-', marker='.', color='b')
        plt.plot(x2_values, y2_values, linestyle='-', marker='.', color='g')
        plt.xlabel(set1['xlabel'])
        plt.ylabel(set1['xlabel'])
        plt.title(title)
        plt.legend([set1['desc'], set2['desc']], loc=legend_loc)

        plt.draw_all()
        savepath = YouthSmokingAnalysis.outputPlotFolderName + "/" + filename
        plt.savefig(savepath)
        plt.clf()

        # plt.show()

    def get_increases(self):
        increases = {}
        for state in self.state_list:
            state_data = self.taxRateDataFrame["STATE"] == state
            start_rate_year = self.taxRateDataFrame["YEAR"] == 2000
            end_rate_year = self.taxRateDataFrame["YEAR"] == 2014
            start_rate = self.taxRateDataFrame[state_data & start_rate_year]["TAX RATE"].values[0]
            end_rate = self.taxRateDataFrame[state_data & end_rate_year]["TAX RATE"].values[0]

            abs_increase = end_rate - start_rate
            pct_increase = ((abs_increase / start_rate) * 100)
            increases[state] = (abs_increase, pct_increase)

        return increases


a = StateAnalysis()
a.analyze()