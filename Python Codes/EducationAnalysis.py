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

    def analyze(self):
        ### Returns a dictionary with the Pandas DFs and Matplitlib Plots
        ### Appends each df and plot to two dictionaries -> 'dataframes' & 'plots' for further use in Python if required.
        response_values = ['Current', 'Ever', 'Frequent']
        gender_values = [True,False]
        cess_measures = ['Percent of Current Smokers Who Want to Quit', 'Quit Attempt in Past Year Among Current Cigarette Smokers']

        result = dict()
        result['dataframes'] = {
            'CigUse' : [],
            'Cessation' : [],
            'SmokelessT' : []
        }
        result['plots'] = {
            'CigUse' : [],
            'Cessation' : [],
            'SmokelessT' : []
        }

        # Analyze Cig Use
        for resp in response_values:
            for gend in gender_values: 
                df = self.analyzeCigUse(response=resp,by_gender=gend)
                result['dataframes']['CigUse'].append(df)
                pl = self.plotCigUse(response=resp,by_gender=gend)
                result['plots']['CigUse'].append(pl)

        # Analyze Cessation
        for measure in cess_measures:
            for gend in gender_values: 
                df = self.analyzeCessation(measure_desc=measure,by_gender=gend)
                result['dataframes']['Cessation'].append(df)
                pl = self.plotCessation(measure_desc=measure,by_gender=gend)
                result['plots']['Cessation'].append(pl)
                
        # Analyze Smokeless Tobacco
        for resp in response_values:
            for gend in gender_values: 
                df = self.analyzeSmokelessTobacco(response=resp,by_gender=gend)
                result['dataframes']['SmokelessT'].append(df)
                pl = self.plotSmokelessTobacco(response=resp,by_gender=gend)
                result['plots']['SmokelessT'].append(pl)
                
        return result



    def analyzeCigUse(self, response='Current', by_gender=False):
        
        ### 
        ### Analyze cigarette use by education level. Can also return by education and gender if by_gender = True
        ### Returns pandas dataframe. Writes df to csv.
        ###         
        ### Parameters:
        ### 
        ### response = 'Current' or 'Frequent' or 'Ever'  (Default = 'Current')
        ### by_gender = True ------------> returns data by education level AND gender (Default = False)
        ###                     False -----------> returns data by education level only
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
            self.outputFile = str(YouthSmokingAnalysis.outputCSVFolderName + '/CigUse_byEdu_%s.csv' % self.response)
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
            self.outputFile = str(YouthSmokingAnalysis.outputCSVFolderName + '/CigUse_byEdu_byGen_%s.csv' % self.response)
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
            self.outputFile = str(YouthSmokingAnalysis.outputCSVFolderName + '/%s_byEdu.csv' % self.measure_desc)
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
            self.outputFile = str(YouthSmokingAnalysis.outputCSVFolderName + '/%s_byEdu_byGen.csv' % self.measure_desc)
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
            self.outputFile = str(YouthSmokingAnalysis.outputCSVFolderName + '/SmokelessT_byEdu_%s.csv' % self.response)
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
            self.outputFile = str(YouthSmokingAnalysis.outputCSVFolderName + '/SmokelessT_byEdu_byGen_%s.csv' % self.response)
            self.dfMAIN.to_csv(self.outputFile, encoding='utf-8',tupleize_cols=True)
            print('Dataframe written to CSV File : ' + self.outputFile)

            return self.dfMAIN

    ####
    #### Plotting
    ####


    def draw_box(self,
                         p,
                         xmin='2012',
                         xmax='2016',
                         alpha = 0.15,
                         color='k',
                         hatch='/',
                         ec='blue'):

        return p.axvspan(xmin=xmin,xmax=xmax,alpha=alpha,color=color,hatch=hatch,ec=ec)
        
    def draw_text(self,
                          p,
                          x=0.97,
                          y=0.95,
                          text='TIPS Campaign',
                          horizontalalignment = 'right',
                          verticalalignment = 'top',
                          multialignment = 'right',
                          fontsize=20,
                          color='red',):

        return p.text(x,y,
               text,
               horizontalalignment=horizontalalignment,
               verticalalignment=verticalalignment,
               multialignment=multialignment,
               fontsize=fontsize,
               color=color,
               transform=p.transAxes)

    def draw_in_subplots(self,p):

        for category in p:
                for sbplot in category:
                    self.draw_box(sbplot)
                    self.draw_text(sbplot,x=0.99,fontsize=12)
        
    def plotCigUse(self, response='Current', by_gender=False):

        self.response = response
        self.by_gender = by_gender
        

        # Call on the analyze_Cig_Use function to return the df for plotting purposes
        self.df = self.analyzeCigUse(self.response,self.by_gender)
        
        # Plot the data by education level only if by_gender is False
        if self.by_gender == False:

            
            p = self.df.plot(figsize=(20,20),
                             style = '-o',
                             title = "Cigaratte Use (%s) by Education " % self.response,
                             x_compat=True,
                             rot = 0
                                   )

            # Adds vertical box & text to indicate POST-Tips Campaign period.

            self.draw_box(p)
            self.draw_text(p)
            
            # Save to File

            self.plot_file = str(YouthSmokingAnalysis.outputPlotFolderName + '/Cig_Use_by_Edu_%s.png' %self.response)
            plt.savefig(self.plot_file)
            print("Plot output to : " + self.plot_file)
            
            return p

        else:
            # Plot the data by education level AND gender level if by_gender is not False

            p = self.df.plot(subplots=True,
                             figsize=(20,20),
                             layout=(2,2),
                             sharey=True,
                             title = "Cigaratte Use (%s) by Education & Gender" % self.response,
                             x_compat=True,
                             rot=0
                         )
            
            # Bifurcate pre/post tips campaign by box and text for each subplot
            self.draw_in_subplots(p)

            
            self.plot_file = str(YouthSmokingAnalysis.outputPlotFolderName + '/Cig_Use_by_Edu_by_Gender_%s.png' % self.response)
            plt.savefig(self.plot_file)
            print("Plot output to : " + self.plot_file)
            
        return p
    
    
    def plotCessation(self, measure_desc, by_gender=False):

        self.measure_desc = measure_desc
        self.by_gender = by_gender
        

        # Call on the analyze_Cig_Use function to return the df for plotting purposes
        self.df = self.analyzeCessation(self.measure_desc,self.by_gender)
        
        # Plot the data by education level only if by_gender is False
        if self.by_gender == False:
            
            p = self.df.plot(figsize=(20,20),
                             style = '-o',
                             title = "%s by Education " % self.measure_desc,
                             x_compat=True,
                             rot=0,
                             )

            # Adds vertical box & text to indicate POST-Tips Campaign period.

            self.draw_box(p)
            self.draw_text(p,y=0.99) # y position of text increased here as it was overlapping with a line
            
            # Save to File

            self.plot_file = str(YouthSmokingAnalysis.outputPlotFolderName + '/%s_by_Edu.png' % self.measure_desc)
            plt.savefig(self.plot_file)
            print("Plot output to : " + self.plot_file)
            
            return p

        else:
        # Plot the data by education level AND gender level if by_gender is not False
            p = self.df.plot(subplots=True,
                             figsize=(20,20), 
                             layout=(2,2), 
                             sharey=True, 
                             title = "%s by Education & Gender" % self.measure_desc,
                             x_compat=True,
                             rot=0,
                        )

            # Bifurcate pre/post tips campaign by box and text for each subplot
            self.draw_in_subplots(p)
            
            # Save to Disk
            self.plot_file = str(YouthSmokingAnalysis.outputPlotFolderName + '/%s_by_Edu_Gen.png' % self.measure_desc)
            plt.savefig(self.plot_file)
            print("Plot output to : " + self.plot_file)
            
            
        return p
    
    def plotSmokelessTobacco(self, response='Current', by_gender=False):

        self.response = response
        self.by_gender = by_gender
        

        # Call on the analyze_Cig_Use function to return the df for plotting purposes
        self.df = self.analyzeSmokelessTobacco(self.response,self.by_gender)
        
        # Plot the data by education level only if by_gender is False
        if self.by_gender == False:
            
            p = self.df.plot(figsize=(20,20),
                             style = '-o',
                             title = "Smokeless Tobacco Use (%s) by Education " % self.response,
                             x_compat=True,
                             rot=0,
                             )

            # Adds vertical box & text to indicate POST-Tips Campaign period.

            self.draw_box(p)
            self.draw_text(p)
            
            # Save to File

            self.plot_file = str(YouthSmokingAnalysis.outputPlotFolderName + '/Smokeless_Tobacco_by_Edu_%s.png' % self.response)
            plt.savefig(self.plot_file)
            print("Plot output to : " + self.plot_file)
            
            return p

        else:
            # Plot the data by education level AND gender level if by_gender is not False
            p = self.df.plot(subplots=True,
                             figsize=(20,20),
                             layout=(2,2),
                             sharey=True,
                             title = "Smokeless Tobacco Use (%s) by Education & Gender" % self.response,
                             x_compat=True,
                             rot=0,
                         )

            # Bifurcate pre/post tips campaign by box and text for each subplot
            self.draw_in_subplots(p)
            
            # Save to Disk
            self.plot_file = str(YouthSmokingAnalysis.outputPlotFolderName + '/Smokeless_Tobacco_by_Edu_by_Gender_%s.png' % self.response)
            plt.savefig(self.plot_file)
            print("Plot output to : " + self.plot_file)

        
        return p


#a = EducationAnalysis()
#results = a.analyze()
#plt.show()
