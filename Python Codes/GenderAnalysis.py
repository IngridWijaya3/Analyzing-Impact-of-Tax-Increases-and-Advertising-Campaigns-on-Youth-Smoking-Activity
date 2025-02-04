import pandas as pd
import numpy
import matplotlib.pyplot as plt
from operator import itemgetter
import datetime
import csv
from YouthSmokingAnalysis import YouthSmokingAnalysis
class GenderAnalysis(YouthSmokingAnalysis):
    
    def __init__(self):
        YouthSmokingAnalysis.__init__(self)
    def analyze(self):
        self.analyzeCigaretteUse()
        self.analyzeCessation()
        self.analyzeBeforeAndAfterCampaign()

        
    def analyzeCigaretteUse(self):
        yearandGenderGroup=self.ytsDataFrame[(self.ytsDataFrame.Gender!='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cigarette Use (Youth)' )
                                             & (self.ytsDataFrame.Response=='Current')]
        # *********************** PERCENTAGE ANALYSIS (analyzeCigaretteUse) **********************
        # group the result by gender
        percentageResult = yearandGenderGroup.groupby(['YEAR','Gender'],as_index=False)
        # find the average percentage of each gender
        df = percentageResult['Data_Value'].mean()
        femaleCigaretteUse = df[df.Gender == 'Female']
        femaleCigaretteUse = femaleCigaretteUse[['YEAR','Data_Value']]
        femaleCigaretteUse = femaleCigaretteUse.rename(columns = {'Data_Value':'Female'})
        femaleCigaretteUse = femaleCigaretteUse.reset_index(drop = True)
        maleCigaretteUse = df[df.Gender == 'Male']
        maleCigaretteUse = maleCigaretteUse[['YEAR','Data_Value']]
        maleCigaretteUse = maleCigaretteUse.rename(columns = {'Data_Value':'Male'})
        maleCigaretteUse = maleCigaretteUse.reset_index(drop = True)
        result_cigUse = pd.concat([femaleCigaretteUse,maleCigaretteUse[['Male']]], axis = 1)
        # save the output in CSV file
        result_cigUse.to_csv('AnalysisCSV/CigaretteUse_result_bygender.csv',index=False)
        # make the values from dataframe to list in order to plot
        femalelist = result_cigUse['Female'].values.tolist()
        malelist = result_cigUse['Male'].values.tolist()
        yearlist = result_cigUse['YEAR'].values.tolist()
        plt.figure(1)
        plt.plot(femalelist,'r--o',label = 'Female')
        plt.plot(malelist,'b--o',label = 'Male')
        x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        plt.xticks(x,yearlist,rotation='vertical')
        plt.legend(loc='upper right')
        plt.xlabel('Year')
        plt.ylabel('Percentage %')
        plt.title('CigaretteUse : Female v.s male from 1999~2015')
        plt.style.use('fivethirtyeight')
        plt.savefig('Plots/CigaretteUse_result_bygender.png')
    
      

        
    def analyzeCessation(self):
        yearandGenderGroup=self.ytsDataFrame[(self.ytsDataFrame.Gender!='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cessation (Youth)')
                                             & (self.ytsDataFrame.MeasureDesc=='Percent of Current Smokers Who Want to Quit') ]
        #*********************** PERCENTAGE ANALYSIS (Cessation) *********************
        # group the result by gender
        percentageResult = yearandGenderGroup.groupby(['YEAR','Gender'],as_index=False)
        # find the average percentage of each gender
        df = percentageResult['Data_Value'].mean()
        femaleCessation = df[df.Gender == 'Female']
        femaleCessation = femaleCessation[['YEAR','Data_Value']]
        femaleCessation = femaleCessation.rename(columns = {'Data_Value':'Female'})
        femaleCessation = femaleCessation.reset_index(drop = True)
        maleCessation = df[df.Gender == 'Male']
        maleCessation = maleCessation[['YEAR','Data_Value']]
        maleCessation = maleCessation.rename(columns = {'Data_Value':'Male'})
        maleCessation = maleCessation.reset_index(drop = True)
        result_Cessation = pd.concat([femaleCessation,maleCessation[['Male']]], axis = 1)
        # save the output in CSV file
        result_Cessation.to_csv('AnalysisCSV/Cessation_result_bygender.csv',index=False)
        # make the values from dataframe to list in order to plot
        femalelist = result_Cessation['Female'].values.tolist()
        malelist = result_Cessation['Male'].values.tolist()
        yearlist = result_Cessation['YEAR'].values.tolist()
        plt.figure(2)
        plt.plot(femalelist,'r--o',label = 'Female')
        plt.plot(malelist,'b--o',label = 'Male')
        x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        plt.xticks(x,yearlist,rotation='vertical')
        plt.legend(loc='upper right')
        plt.xlabel('Year')
        plt.ylabel('Percentage %')
        plt.title('Percent of Current Smokers Who Want to Quit 1999~2015')
        plt.style.use('fivethirtyeight')
        plt.savefig('Plots/Cessation_result_bygender.png')

        
    def analyzeBeforeAndAfterCampaign(self):
        yearandGenderGroup=self.ytsDataFrame[(self.ytsDataFrame.Gender!='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cigarette Use (Youth)' )
                                             & (self.ytsDataFrame.Response=='Current')]
        #*********************** PERCENTAGE ANALYSIS (Before and After Campaign) **********************        # group the result by gender
        percentageResult = yearandGenderGroup.groupby(['YEAR','Gender'],as_index=False)
        # find the average percentage of each gender
        df = percentageResult['Data_Value'].mean()
        femaleCigaretteUse = df[df.Gender == 'Female']
        femaleCigaretteUse = femaleCigaretteUse[['YEAR','Data_Value']]
        femaleCigaretteUse = femaleCigaretteUse.rename(columns = {'Data_Value':'Female'})
        femaleCigaretteUse = femaleCigaretteUse.reset_index(drop = True)
        maleCigaretteUse = df[df.Gender == 'Male']
        maleCigaretteUse = maleCigaretteUse[['YEAR','Data_Value']]
        maleCigaretteUse = maleCigaretteUse.rename(columns = {'Data_Value':'Male'})
        # since we select out female and male, reset the index for each gender
        maleCigaretteUse = maleCigaretteUse.reset_index(drop = True)
        result_cigUse = pd.concat([femaleCigaretteUse,maleCigaretteUse[['Male']]], axis = 1)
        # average out the percentage before and after 2012 (start of Campaign)
        before_result_cigUse = result_cigUse[result_cigUse.YEAR < 2012]
        after_result_cigUse = result_cigUse[result_cigUse.YEAR >= 2012]
        before_femaleresult = before_result_cigUse['Female'].mean()
        before_maleresult = before_result_cigUse['Male'].mean()
        after_femaleresult = after_result_cigUse['Female'].mean()
        after_maleresult = after_result_cigUse['Male'].mean()
        raw_data = {'Time':['Before 2012','After 2012'],
                             'Female':[before_femaleresult,after_femaleresult],
                             'Male':[before_maleresult,after_maleresult]}
        before_after_result = pd.DataFrame(raw_data, columns = ['Time','Female','Male'])
        # save the output in CSV file
        before_after_result.to_csv('AnalysisCSV/before_after_result_bygender.csv',index = False)
        femaleavg = (before_femaleresult,after_femaleresult)
        maleavg = (before_maleresult,after_maleresult)
        ax = before_after_result[['Female','Male']].plot(kind = 'bar', title = "Before and After Campaign Bar Plot")
        ax.set_xlabel("Before and After Campaign")
        ax.set_ylabel("Percentage %")
        ax.set_xticklabels(('before','after'),rotation='horizontal')
        plt.style.use('fivethirtyeight')
        plt.savefig('Plots/before_after_result_bygender.png')
        

        
        


