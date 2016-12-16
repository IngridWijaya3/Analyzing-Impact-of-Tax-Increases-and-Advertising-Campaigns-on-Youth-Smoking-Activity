## YTS Analysis by Education level

import pandas
import numpy
import matplotlib.pyplot as plt
import datetime
from YouthSmokingAnalysis import YouthSmokingAnalysis
plt.style.use('fivethirtyeight')
pandas.options.mode.chained_assignment = None

class EducationAnalysis(YouthSmokingAnalysis): # inherit from the superclass
    
    def __init__(self):
        YouthSmokingAnalysis.__init__(self)

    def analyze(self, response='Current', by_gender=False):
        
        ### 
        ### Analyze cigarette use by education level. Can also return by education and gender if by_gender = True
        ### Returns pandas dataframe. Writes df to csv.
        ###         
        ### Parameters:
        ### 
        ### response = 'Current' or 'Frequent' or 'Ever'  (Default = 'Current')
        ### by_gender = True ------------> returns data by education level AND gender (Default = False)
        ###             False -----------> returns data by education level only
        ###
        
        self.response = response
        self.by_gender = by_gender
        
        if by_gender is False:
            
            self.dfMAIN = self.ytsDataFrame[ (self.ytsDataFrame.Gender == 'Overall')
                                                 & (self.ytsDataFrame.TopicDesc == 'Cigarette Use (Youth)')
                                                 & (self.ytsDataFrame.MeasureDesc == 'Smoking Status')
                                                 & (self.ytsDataFrame.Response == self.response)
                                           ]
            
            # Convert the 'YEAR' column to time series - Makes plotting easier with Pandas/Matplotlib
            self.date = pandas.to_datetime({'Year' : self.dfMAIN.YEAR, 'Month' : 1, 'Day' : 1})
            self.dfMAIN['Date'] = self.date
            
            # Drop columns not needed in this analysis
            self.dfMAIN = self.dfMAIN[['Date','Data_Value','Education']]
            
            # Create pivot table of our Data Frame
            self.dfMAIN = pandas.pivot_table(self.dfMAIN.reset_index(),
                           index='Date', columns='Education', values='Data_Value', aggfunc='mean',
                                           )
            
            # Fill NaN with mean
            self.dfMAIN = self.dfMAIN.fillna(self.dfMAIN[(self.dfMAIN.index == self.dfMAIN.index)].mean())
            
            # Write to CSV
            self.outputFile = str('AnalysisCSV/CigUse_byEdu_%s.csv' % self.response)
            self.dfMAIN.to_csv(self.outputFile, encoding='utf-8')
            print('Dataframe written to CSV File : ' + self.outputFile)

            return self.dfMAIN
            
        else:
            
            self.dfMAIN = self.ytsDataFrame[ (self.ytsDataFrame.Gender != 'Overall')
                                                 & (self.ytsDataFrame.TopicDesc == 'Cigarette Use (Youth)')
                                                 & (self.ytsDataFrame.MeasureDesc == 'Smoking Status')
                                                 & (self.ytsDataFrame.Response == self.response)
                                           ]
            
            # Convert the 'YEAR' column to time series - Makes plotting easier with Pandas/Matplotlib
            self.date = pandas.to_datetime({'Year' : self.dfMAIN.YEAR, 'Month' : 1, 'Day' : 1})
            self.dfMAIN['Date'] = self.date
            
            # Drop columns not needed in this analysis
            self.dfMAIN = self.dfMAIN[['Date','Data_Value','Education','Gender']]
            
            # Create pivot table of our Data Frame
            self.dfMAIN = pandas.pivot_table(self.dfMAIN.reset_index(),
                           index='Date', columns=['Education','Gender'], values='Data_Value', aggfunc='mean'
                            )
            
            # Fill NaN with mean
            self.dfMAIN = self.dfMAIN.fillna(self.dfMAIN[(self.dfMAIN.index == self.dfMAIN.index)].mean())
            
            # Write to CSV
            self.outputFile = str('AnalysisCSV/CigUse_byEdu_byGen_%s.csv' % self.response)
            self.dfMAIN.to_csv(self.outputFile, encoding='utf-8',tupleize_cols=True)
            print('Dataframe written to CSV File : ' + self.outputFile)

            return self.dfMAIN
        
    def analyzeCessation(self, measure_desc, by_gender=False):
        
        ###  Returns Cessation Data by Education level.
        ###  Can also return by gender and education if by_gender=True
        ### 
        ###  Paramaters:
        ###  measure_desc <---> Choose from :
        ###  "Percent of Current Smokers Who Want to Quit" or "Quit Attempt in Past Year Among Current Cigarette Smokers"
        ### 
        
        self.measure_desc = measure_desc
        self.by_gender = by_gender
        
        if self.by_gender == False:
            
            # Select columns that are required for this analysis 
            self.dfMAIN = self.ytsDataFrame[ (self.ytsDataFrame.Gender == 'Overall')
                                                 & (self.ytsDataFrame.TopicDesc == 'Cessation (Youth)' )
                                                 & (self.ytsDataFrame.MeasureDesc == self.measure_desc )
                                                 ]

            # Convert the 'YEAR' column to time series - Makes plotting easier with Pandas/Matplotlib
            self.date = pandas.to_datetime({'Year' : self.dfMAIN.YEAR, 'Month' : 1, 'Day' : 1})
            self.dfMAIN['Date'] = self.date
            
            # Drop columns not needed in this analysis
            self.dfMAIN = self.dfMAIN[['Date','Data_Value','Education']]

            # Create pivot table of our Data Frame
            self.dfMAIN = pandas.pivot_table(self.dfMAIN.reset_index(),
                           index='Date', columns='Education', values='Data_Value', aggfunc='mean',
                          )
            
            # Fill NaN with mean
            self.dfMAIN = self.dfMAIN.fillna(self.dfMAIN[(self.dfMAIN.index == self.dfMAIN.index)].mean())
            
            # Write to CSV
            self.outputFile = str('AnalysisCSV/%s_byEdu.csv' % self.measure_desc)
            self.dfMAIN.to_csv(self.outputFile, encoding='utf-8')
            print('Dataframe written to CSV File : ' + self.outputFile)

            return self.dfMAIN
        
        else:

            # Select columns that are required for this analysis 
            self.dfMAIN = self.ytsDataFrame[ (self.ytsDataFrame.Gender != 'Overall')
                                                 & (self.ytsDataFrame.TopicDesc == 'Cessation (Youth)' )
                                                 & (self.ytsDataFrame.MeasureDesc == self.measure_desc )
                                                 ]

            # Convert the 'YEAR' column to time series - Makes plotting easier with Pandas/Matplotlib
            self.date = pandas.to_datetime({'Year' : self.dfMAIN.YEAR, 'Month' : 1, 'Day' : 1})
            self.dfMAIN['Date'] = self.date
            
            # Drop columns not needed in this analysis
            self.dfMAIN = self.dfMAIN[['Date','Data_Value','Education','Gender']]

            # Create pivot table of our Data Frame
            self.dfMAIN = pandas.pivot_table(self.dfMAIN.reset_index(),
                           index='Date', columns=['Education','Gender'], values='Data_Value', aggfunc='mean',
                          )
            
            # Fill NaN with mean
            self.dfMAIN = self.dfMAIN.fillna(self.dfMAIN[(self.dfMAIN.index == self.dfMAIN.index)].mean())
            
            # Write to CSV
            self.outputFile = str('AnalysisCSV/%s_byEdu_byGen.csv' % self.measure_desc)
            self.dfMAIN.to_csv(self.outputFile, encoding='utf-8',tupleize_cols=True)
            print('Dataframe written to CSV File : ' + self.outputFile)

            return self.dfMAIN
    
    
    def analyzeSmokelessTobacco(self, response, by_gender=False):
        
        ### 
        ### Analayze Smokeless Tobacco Use
        ### Default is by education level. Can also return by education and gender if by_gender = True.
        ### Returns pandas dataframe. Writes df to csv.
        ###         
        ### Parameters:
        ### 
        ### response = 'Current' or 'Frequent' or 'Ever'  (Default = 'Current')
        ### by_gender = True ------------> returns data by education level AND gender (Default = False)
        ###             False -----------> returns data by education level only
        ###
        
        self.response = response
        self.by_gender = by_gender
        
        if by_gender is False:
            
            self.dfMAIN = self.ytsDataFrame[ (self.ytsDataFrame.Gender == 'Overall')
                                                 & (self.ytsDataFrame.TopicDesc == 'Smokeless Tobacco Use (Youth)')
                                                 & (self.ytsDataFrame.MeasureDesc == 'User Status')
                                                 & (self.ytsDataFrame.Response == self.response)
                                           ]
            
            # Convert the 'YEAR' column to time series - Makes plotting easier with Pandas/Matplotlib
            self.date = pandas.to_datetime({'Year' : self.dfMAIN.YEAR, 'Month' : 1, 'Day' : 1})
            self.dfMAIN['Date'] = self.date
            
            # Drop columns not needed in this analysis
            self.dfMAIN = self.dfMAIN[['Date','Data_Value','Education']]
            
            # Create pivot table of our Data Frame
            self.dfMAIN = pandas.pivot_table(self.dfMAIN.reset_index(),
                           index='Date', columns='Education', values='Data_Value', aggfunc='mean',
                                           )
            
            # Fill NaN with mean
            self.dfMAIN = self.dfMAIN.fillna(self.dfMAIN[(self.dfMAIN.index == self.dfMAIN.index)].mean())
            
            # Write to CSV
            self.outputFile = str('AnalysisCSV/SmokelessT_byEdu_%s.csv' % self.response)
            self.dfMAIN.to_csv(self.outputFile, encoding='utf-8')
            print('Dataframe written to CSV File : ' + self.outputFile)

            return self.dfMAIN
            
        else:
            
            self.dfMAIN = self.ytsDataFrame[ (self.ytsDataFrame.Gender != 'Overall')
                                                 & (self.ytsDataFrame.TopicDesc == 'Smokeless Tobacco Use (Youth)')
                                                 & (self.ytsDataFrame.MeasureDesc == 'User Status')
                                                 & (self.ytsDataFrame.Response == self.response)
                                           ]
            
            # Convert the 'YEAR' column to time series - Makes plotting easier with Pandas/Matplotlib
            self.date = pandas.to_datetime({'Year' : self.dfMAIN.YEAR, 'Month' : 1, 'Day' : 1})
            self.dfMAIN['Date'] = self.date
            
            # Drop columns not needed in this analysis
            self.dfMAIN = self.dfMAIN[['Date','Data_Value','Education','Gender']]
            
            # Create pivot table of our Data Frame
            self.dfMAIN = pandas.pivot_table(self.dfMAIN.reset_index(),
                           index='Date', columns=['Education','Gender'], values='Data_Value', aggfunc='mean'
                            )
            
            # Fill NaN with mean
            self.dfMAIN = self.dfMAIN.fillna(self.dfMAIN[(self.dfMAIN.index == self.dfMAIN.index)].mean())
            
            # Write to CSV
            self.outputFile = str('AnalysisCSV/SmokelessT_byEdu_byGen_%s.csv' % self.response)
            self.dfMAIN.to_csv(self.outputFile, encoding='utf-8',tupleize_cols=True)
            print('Dataframe written to CSV File : ' + self.outputFile)

            return self.dfMAIN
    
    def analyzeBeforeAndAfterCampaign(self):
        
        print("add codes here")
        
    def analyzeBeforeAndAfterTax(self):
        
        print("add codes here")
        
    def plotCigUse(self, response='Current', by_gender=False):

        self.response = response
        self.by_gender = by_gender

        # Call on the analyze_Cig_Use function to return the df for plotting purposes
        self.df = self.analyze(self.response,self.by_gender)
        
        # Plot the data by education level only if by_gender is False
        if self.by_gender == False:
            
            self.df.plot(figsize=(20,20),
                                   style = '--o',
                                   title = "Cigaratte Use (%s) by Education " % self.response,
                                   )

            self.plot_file = str('Plots/Cig_Use_by_Edu_%s.png' %self.response)
            plt.savefig(self.plot_file)
            print("Plot output to : " + self.plot_file)
            
            return plt.show()

        else:
        # Plot the data by education level AND gender level if by_gender is not False
            self.df.plot(subplots=True, 
                         figsize=(20,20), 
                         layout=(2,2), 
                         sharey=True, 
                         title = "Cigaratte Use (%s) by Education & Gender" % self.response,
                         )

            
            self.plot_file = str('Plots/Cig_Use_by_Edu_by_Gender_%s.png' % self.response)
            plt.savefig(self.plot_file)
            print("Plot output to : " + self.plot_file)
            
        return plt.show()
    
    
    def plotCessation(self, measure_desc, by_gender=False):

        self.measure_desc = measure_desc
        self.by_gender = by_gender

        # Call on the analyze_Cig_Use function to return the df for plotting purposes
        self.df = self.analyzeCessation(self.measure_desc,self.by_gender)
        
        # Plot the data by education level only if by_gender is False
        if self.by_gender == False:
            
            self.df.plot(figsize=(20,20),
                                   style = '--o',
                                   title = "%s by Education " % self.measure_desc,
                                   )

            self.plot_file = str('Plots/%s_by_Edu.png' % self.measure_desc)
            plt.savefig(self.plot_file)
            print("Plot output to : " + self.plot_file)
            
            return plt.show()

        else:
        # Plot the data by education level AND gender level if by_gender is not False
            self.df.plot(subplots=True, 
                         figsize=(20,20), 
                         layout=(2,2), 
                         sharey=True, 
                         title = "%s by Education & Gender" % self.measure_desc
                        )

            self.plot_file = str('Plots/%s_by_Edu_Gen.png' % self.measure_desc)
            plt.savefig(self.plot_file)
            print("Plot output to : " + self.plot_file)
            
            
        return plt.show()
    
    def plotSmokelessTobacco(self, response='Current', by_gender=False):

        self.response = response
        self.by_gender = by_gender

        # Call on the analyze_Cig_Use function to return the df for plotting purposes
        self.df = self.analyzeSmokelessTobacco(self.response,self.by_gender)
        
        # Plot the data by education level only if by_gender is False
        if self.by_gender == False:
            
            self.df.plot(figsize=(20,20),
                                   style = '--o',
                                   title = "Smokeless Tobacco Use (%s) by Education " % self.response,
                                   )

            self.plot_file = str('Plots/Smokeless_Tobacco_by_Edu_%s.png' % self.response)
            plt.savefig(self.plot_file)
            print("Plot output to : " + self.plot_file)
            
            return plt.show()

        else:
            # Plot the data by education level AND gender level if by_gender is not False
            
            self.df.plot(subplots=True, 
                         figsize=(20,20), 
                         layout=(2,2), 
                         sharey=True, 
                         title = "Smokeless Tobacco Use (%s) by Education & Gender" % self.response,
                         )
            
            self.plot_file = str('Plots/Smokeless_Tobacco_by_Edu_by_Gender_%s.png' % self.response )
            plt.savefig(self.plot_file)
            print("Plot output to : " + self.plot_file)
            
        return plt.show()


Analysis = EducationAnalysis()
### Write our analysis to CSVs. 
### Also appends each df to 'dataframes' dictionary for further use in Python.

response_values = ['Current', 'Ever', 'Frequent']
gender_values = [True,False]
cess_measures = ['Percent of Current Smokers Who Want to Quit', 'Quit Attempt in Past Year Among Current Cigarette Smokers']

dataframes = {
    'CigUse' : [],
    'Cessation' : [],
    'SmokelessT' : []
}

plots = {
    'CigUse' : [],
    'Cessation' : [],
    'SmokelessT' : []
}

'''
Need to put the code below in a main() function
'''

# Analyze Cig Use
for resp in response_values:
    for gend in gender_values: 
        df = Analysis.analyze(response=resp,by_gender=gend)
        dataframes['CigUse'].append(df)

# Analyze Cessation
for measure in cess_measures:
    for gend in gender_values: 
        df = Analysis.analyzeCessation(measure_desc=measure,by_gender=gend)
        dataframes['Cessation'].append(df)
        
# Analyze Smokeless Tobacco
for resp in response_values:
    for gend in gender_values: 
        df = Analysis.analyzeSmokelessTobacco(response=resp,by_gender=gend)
        dataframes['SmokelessT'].append(df)
        
        
### Create Plots for our analysis and save them to disk.
### Also appends plots to a dict for further use in Python

# Analyze Cig Use
for resp in response_values:
    for gend in gender_values: 
        pl = Analysis.plotCigUse(response=resp,by_gender=gend)
        plots['CigUse'].append(pl)

# Analyze Cessation
for measure in cess_measures:
    for gend in gender_values: 
        pl = Analysis.plotCessation(measure_desc=measure,by_gender=gend)
        plots['Cessation'].append(pl)
        
# Analyze Smokeless Tobacco
for resp in response_values:
    for gend in gender_values: 
        pl = Analysis.plotSmokelessTobacco(response=resp,by_gender=gend)
        plots['SmokelessT'].append(pl)
