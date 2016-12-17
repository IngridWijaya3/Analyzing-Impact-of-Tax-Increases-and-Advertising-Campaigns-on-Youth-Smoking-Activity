
import pandas
import numpy
import matplotlib.pyplot as plt
import datetime
from YouthSmokingAnalysis import YouthSmokingAnalysis

class StateCampaignAnalysis(YouthSmokingAnalysis):
    
    def __init__(self):
        YouthSmokingAnalysis.__init__(self)
        
    def analyze(self):
        self.analyzeCigaretteUse()
        self.analyzeCessation()
        self.analyzeBeforeAndAfterCampaign()
        self.plotBeforeAndAfterCampaign(self.stateCigaretteUseResult,"Cigarette Use")
        self.plotBeforeAndAfterCampaign(self.stateSmokelessTobaccoUseResult,"Smokelese Tobacco")
        self.plotBeforeAndAfterCampaign(self.stateCessationTobaccoUseResult,"Cessation")
        self.plotCigaretteUseAfterCampaign()
        
    def analyzeCessation(self):
        self.stateAndCessation=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cessation (Youth)')
                                             & (self.ytsDataFrame.YEAR>2012)][['YEAR','LocationAbbr','MeasureDesc','Data_Value']].groupby(['LocationAbbr','MeasureDesc'], as_index=False)['Data_Value'].mean()
        self.stateAndCessation=self.stateAndCessation.sort_values(by=['LocationAbbr'], ascending=True)
        self.stateAndCessation=pandas.pivot_table(self.stateAndCessation, index=['LocationAbbr'], columns=['MeasureDesc'] , values='Data_Value')
        self.stateAndCessation.rename(columns={"Percent of Current Smokers Who Want to Quit": "Percent of Current Smokers Who Want to Quit After Campaign",
                                               "Quit Attempt in Past Year Among Current Cigarette Smokers":"Quit Attempt in Past Year Among Current Cigarette Smokers After Campaign"},inplace=True)
        self.stateAndCessation.reset_index( inplace=True)

        self.stateAndCessationBC=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cessation (Youth)')
                                             & (self.ytsDataFrame.YEAR<=2012)][['YEAR','LocationAbbr','MeasureDesc','Data_Value']].groupby(['LocationAbbr','MeasureDesc'], as_index=False)['Data_Value'].mean()
        self.stateAndCessationBC=self.stateAndCessationBC.sort_values(by=['LocationAbbr'], ascending=True)
        self.stateAndCessationBC=pandas.pivot_table(self.stateAndCessationBC, index=['LocationAbbr'], columns=['MeasureDesc'] , values='Data_Value')
        self.stateAndCessationBC.rename(columns={"Percent of Current Smokers Who Want to Quit": "Percent of Current Smokers Who Want to Quit Before Campaign",
                                               "Quit Attempt in Past Year Among Current Cigarette Smokers":"Quit Attempt in Past Year Among Current Cigarette Smokers Before Campaign"},inplace=True)
        
        self.stateAndCessationBC.reset_index( inplace=True)
        self.stateAndCessationCombine=pandas.merge( self.stateAndCessationBC, self.stateAndCessation, left_on=['LocationAbbr'], right_on=['LocationAbbr'])
        print(self.stateAndCessationBC)

        outputFilePath = str(YouthSmokingAnalysis.outputCSVFolderName+'/State and Cessation Who Want to Quit VS Quit Attempt.csv')
        
        self.stateAndCessationCombine.to_csv(outputFilePath, encoding='utf-8')

        
    def analyzeCigaretteUse(self):
        self.stateAndCigaretteUse=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cigarette Use (Youth)')
                                             & (self.ytsDataFrame.YEAR>2012)][['YEAR','LocationAbbr','MeasureDesc','Response','Data_Value']]
        self.stateAndCigaretteUse['CigaretteUseStatus'] = self.stateAndCigaretteUse[['MeasureDesc', 'Response']].apply(lambda x: ' '.join(x), axis=1)
        
        self.stateAndCigaretteUse=self.stateAndCigaretteUse.groupby(['LocationAbbr','CigaretteUseStatus'], as_index=False)['Data_Value'].mean()
        self.stateAndCigaretteUse=self.stateAndCigaretteUse.sort_values(by=['LocationAbbr'], ascending=True)
        self.stateAndCigaretteUse=pandas.pivot_table(self.stateAndCigaretteUse, index=['LocationAbbr'], columns=['CigaretteUseStatus'] , values='Data_Value')
        self.stateAndCigaretteUse.rename(columns={"Smoking Status Frequent": "Frequent After Campaign",
                                                                "Smoking Status Current":"Current After Campaign",
                                                                "Smoking Status Ever": "Ever After Campaign"},inplace=True)
        self.stateAndCigaretteUse.reset_index( inplace=True)

        self.stateAndCigaretteUseBC=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cigarette Use (Youth)')
                                             & (self.ytsDataFrame.YEAR<=2012)][['YEAR','LocationAbbr','MeasureDesc','Response','Data_Value']]
        self.stateAndCigaretteUseBC['CigaretteUseStatus'] = self.stateAndCigaretteUseBC[['MeasureDesc', 'Response']].apply(lambda x: ' '.join(x), axis=1)
        
        self.stateAndCigaretteUseBC=self.stateAndCigaretteUseBC.groupby(['LocationAbbr','CigaretteUseStatus'], as_index=False)['Data_Value'].mean()
        self.stateAndCigaretteUseBC=self.stateAndCigaretteUseBC.sort_values(by=['LocationAbbr'], ascending=True)
      
        self.stateAndCigaretteUseBC=pandas.pivot_table(self.stateAndCigaretteUseBC, index=['LocationAbbr'], columns=['CigaretteUseStatus'] , values='Data_Value')
        self.stateAndCigaretteUseBC.rename(columns={"Smoking Status Frequent": "Frequent Before Campaign",
                                                                "Smoking Status Current":"Current Before Campaign",
                                                                "Smoking Status Ever": "Ever Before Campaign"},inplace=True)
        self.stateAndCigaretteUseBC.reset_index( inplace=True)
 
        self.stateAndCigaretteUseResponseCombine=pandas.merge( self.stateAndCigaretteUseBC, self.stateAndCigaretteUse, left_on=['LocationAbbr'], right_on=['LocationAbbr'])
        outputFilePath = str(YouthSmokingAnalysis.outputCSVFolderName+'/State and Cigarette Use Response Before and After Campaign.csv')
 
        self.stateAndCigaretteUseResponseCombine.to_csv(outputFilePath, encoding='utf-8')

    def plotCigaretteUseAfterCampaign(self):
        
        plt.style.use('fivethirtyeight')

        n_groups = len(self.stateAndCigaretteUse.index)
        
        SmokingStatusFrequent = self.stateAndCigaretteUse["Frequent After Campaign"].values
        SmokingStatusCurrent= self.stateAndCigaretteUse["Current After Campaign"].values
        SmokingStatusEver= self.stateAndCigaretteUse["Ever After Campaign"].values
           

        fig, ax = plt.subplots()
        fig.set_figheight(20)
        fig.set_figwidth(50)
        
        index = numpy.arange(n_groups)
        index = numpy.arange(0, n_groups * 2, 2)
        bar_width = 0.35

        opacity = 0.4
        error_config = {'ecolor': '0.3'}

        rects1 = plt.bar(index, SmokingStatusFrequent, bar_width,
                     alpha=opacity,
                     color='b',
                     error_kw=error_config,
                     label='Smoking Status Frequent')

        rects2 = plt.bar(index + bar_width, SmokingStatusCurrent, bar_width,
                     alpha=opacity,
                     color='r',
                     error_kw=error_config,
                     label='Smoking Status Current')
        
        rects3 = plt.bar(index + bar_width+ bar_width, SmokingStatusEver, bar_width,
                     alpha=opacity,
                     color='y',
                     error_kw=error_config,
                     label='Smoking Status Ever')

        plt.xlabel('States')
        plt.ylabel('Percent Average')
        plt.title('Percent Average Cigarette Use Response After Campaign')
        plt.xticks(index + bar_width+ bar_width, self.stateAndCigaretteUse.LocationAbbr,fontsize=20)
       
        plt.legend()

        plt.savefig(YouthSmokingAnalysis.outputPlotFolderName+'/State and Cigarette Use Response Before And After Campaign.png')
        

    
    def analyzeBeforeAndAfterCampaign(self):
       
        self.stateAndCigaretteUseAfterCampaign=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cigarette Use (Youth)' )
                                             & (self.ytsDataFrame.MeasureDesc=='Smoking Status')
                                             & (self.ytsDataFrame.YEAR>2012)][['YEAR','LocationAbbr','Data_Value']]
        self.stateAndCigaretteUseAfterCampaign=self.stateAndCigaretteUseAfterCampaign.rename(columns={"Data_Value": "AverageAfterCampaign"}).groupby(['LocationAbbr'])['AverageAfterCampaign'].mean()
        
        self.stateAndCigaretteUseBeforeCampaign=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cigarette Use (Youth)' )
                                             & (self.ytsDataFrame.MeasureDesc=='Smoking Status')
                                             & (self.ytsDataFrame.YEAR<=2012)][['YEAR','LocationAbbr','Data_Value']]
        self.stateAndCigaretteUseBeforeCampaign=self.stateAndCigaretteUseBeforeCampaign.rename(columns={"Data_Value": "AverageBeforeCampaign"}).groupby(['LocationAbbr'])['AverageBeforeCampaign'].mean()
      
 
        self.stateCigaretteUseResult= pandas.concat([self.stateAndCigaretteUseBeforeCampaign,self.stateAndCigaretteUseAfterCampaign ],axis=1)
        self.stateCigaretteUseResult["PercentDecrease"]=((self.stateCigaretteUseResult.AverageBeforeCampaign-self.stateCigaretteUseResult.AverageAfterCampaign)/self.stateCigaretteUseResult.AverageBeforeCampaign)*100
        self.stateCigaretteUseResult=self.stateCigaretteUseResult.sort_values(by='PercentDecrease', ascending=False)

        self.stateAndSmokelessTobaccoUseBeforeCampaign=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Smokeless Tobacco Use (Youth)' )
                                             & (self.ytsDataFrame.YEAR<=2012)][['YEAR','LocationAbbr','Data_Value']]
        self.stateAndSmokelessTobaccoUseBeforeCampaign=self.stateAndSmokelessTobaccoUseBeforeCampaign.rename(columns={"Data_Value": "AverageBeforeCampaign"}).groupby(['LocationAbbr'])['AverageBeforeCampaign'].mean()

        self.stateAndSmokelessTobaccoUseAfterCampaign=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Smokeless Tobacco Use (Youth)' )
                                             & (self.ytsDataFrame.YEAR>2012)][['YEAR','LocationAbbr','Data_Value']].rename(columns={"Data_Value": "AverageAfterCampaign"}).groupby(['LocationAbbr'])['AverageAfterCampaign'].mean()

        self.stateSmokelessTobaccoUseResult= pandas.concat([self.stateAndSmokelessTobaccoUseBeforeCampaign,self.stateAndSmokelessTobaccoUseAfterCampaign],axis=1)
        self.stateSmokelessTobaccoUseResult["PercentDecrease"]=((self.stateSmokelessTobaccoUseResult.AverageBeforeCampaign-self.stateSmokelessTobaccoUseResult.AverageAfterCampaign)/self.stateSmokelessTobaccoUseResult.AverageBeforeCampaign)*100
        self.stateSmokelessTobaccoUseResult=self.stateSmokelessTobaccoUseResult.sort_values(by='PercentDecrease', ascending=False)
        
        self.stateAndCessationBeforeCampaign=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cessation (Youth)' )
                                             & (self.ytsDataFrame.YEAR<=2012)][['YEAR','LocationAbbr','Data_Value']]
        self.stateAndCessationBeforeCampaign=self.stateAndCessationBeforeCampaign.rename(columns={"Data_Value": "AverageBeforeCampaign"}).groupby(['LocationAbbr'])['AverageBeforeCampaign'].mean()

        self.stateAndCessationAfterCampaign=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cessation (Youth)' )
                                             & (self.ytsDataFrame.YEAR>2012)][['YEAR','LocationAbbr','Data_Value']]
        self.stateAndCessationAfterCampaign=self.stateAndCessationAfterCampaign.rename(columns={"Data_Value": "AverageAfterCampaign"}).groupby(['LocationAbbr'])['AverageAfterCampaign'].mean()

        self.stateCessationTobaccoUseResult= pandas.concat([self.stateAndCessationBeforeCampaign,self.stateAndCessationAfterCampaign],axis=1)
        self.stateCessationTobaccoUseResult["PercentIncrease"]=((self.stateCessationTobaccoUseResult.AverageAfterCampaign-self.stateCessationTobaccoUseResult.AverageBeforeCampaign)/self.stateCessationTobaccoUseResult.AverageBeforeCampaign)*100
        self.stateCessationTobaccoUseResult=self.stateCessationTobaccoUseResult.sort_values(by='PercentIncrease', ascending=False)
        
        outputFilePath = str(YouthSmokingAnalysis.outputCSVFolderName+'/State and Cigarette User Before and After Campaign.csv')
        self.stateCigaretteUseResult.to_csv(outputFilePath, encoding='utf-8')
        outputFilePath = str(YouthSmokingAnalysis.outputCSVFolderName+'/State and Smokeless Tobacco Before and After Campaign.csv')
        self.stateSmokelessTobaccoUseResult.to_csv(outputFilePath, encoding='utf-8')
        outputFilePath = str(YouthSmokingAnalysis.outputCSVFolderName+'/State and Cessation Before and After Campaign.csv')
        self.stateCessationTobaccoUseResult.to_csv(outputFilePath, encoding='utf-8')

    def plotBeforeAndAfterCampaign(self,df,title):

        plt.style.use('fivethirtyeight')

        n_groups = len(df.index)

        averagePercentBeforeCampaign = df["AverageBeforeCampaign"].values
        averagePercentAfterCampaign = df["AverageAfterCampaign"].values

        fig, ax = plt.subplots()
        fig.set_figheight(20)
        fig.set_figwidth(50)
        
        index = numpy.arange(n_groups)
        index = numpy.arange(0, n_groups * 2, 2)
        bar_width = 0.35

        opacity = 0.4
        error_config = {'ecolor': '0.3'}

        rects1 = plt.bar(index, averagePercentBeforeCampaign, bar_width,
                     alpha=opacity,
                     color='b',
                     error_kw=error_config,
                     label='Before Campaign')

        rects2 = plt.bar(index + bar_width, averagePercentAfterCampaign, bar_width,
                     alpha=opacity,
                     color='r',
                     error_kw=error_config,
                     label='After Campaign')

        plt.xlabel('States')
        plt.ylabel('Percent Average')
        plt.title('Percent Average '+title+ ' Before And After Campaign')
        plt.xticks(index + bar_width, df.index,fontsize=20)
       
        plt.legend()

        #plt.show()
        plt.savefig(YouthSmokingAnalysis.outputPlotFolderName+'/State And '+title+' Before And After Campaign.png')

a = StateCampaignAnalysis()
a.analyze()

        




