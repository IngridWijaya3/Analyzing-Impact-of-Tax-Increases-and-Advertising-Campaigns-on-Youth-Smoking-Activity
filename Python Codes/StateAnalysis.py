
import pandas
import numpy
import matplotlib 
import datetime
from YouthSmokingAnalysis import YouthSmokingAnalysis

class StateAnalysis(YouthSmokingAnalysis):
    
    def __init__(self):
        YouthSmokingAnalysis.__init__(self)
    def analyze(self):
        yearandStateGroup=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cigarette Use (Youth)' )
                                             & (self.ytsDataFrame.MeasureDesc=='Smoking Status')]
       
        print(yearandStateGroup[['YEAR','LocationAbbr','Data_Value']])
        numberOfPeopleSmoking=yearandStateGroup.groupby(['YEAR','LocationAbbr'], as_index=False)['Data_Value'].mean()
        pivotTable=pandas.pivot_table(numberOfPeopleSmoking, index=['YEAR'], columns=['LocationAbbr'] , values='Data_Value')


        print(numberOfPeopleSmoking)
        print(pivotTable)
        return numberOfPeopleSmoking
    def analyzeCessation(self):
        print("add codes here")
    def analyzeNonCessation(self):
        print("add codes here")
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
        
        print(self.stateCigaretteUseResult)
        print(self.stateSmokelessTobaccoUseResult)
        print(self.stateCessationTobaccoUseResult)


        
    def analyzeBeforeAndAfterTax(self):
        print("add codes here")
    def plotResult(self):
        print("add codes here")

a=StateAnalysis()
a.analyzeBeforeAndAfterCampaign()

