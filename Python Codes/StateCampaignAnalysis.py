
import pandas
import numpy
import matplotlib 
import datetime
from YouthSmokingAnalysis import YouthSmokingAnalysis

class StateCampaignAnalysis(YouthSmokingAnalysis):
    
    def __init__(self):
        YouthSmokingAnalysis.__init__(self)
        
    def analyze(self):
        self.analyzeCigaretteUse()
        self.analyzeCessation()
        self.analyzeBeforeAndAfterCampaign()
        
    def analyzeCessation(self):
        self.stateAndCessation=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cessation (Youth)' )][['YEAR','LocationAbbr','MeasureDesc','Data_Value']].groupby(['YEAR','LocationAbbr','MeasureDesc'], as_index=False)['Data_Value'].mean()
        self.stateAndCessation=self.stateAndCessation.sort_values(by=['YEAR','LocationAbbr'], ascending=False)
        self.stateAndCessation=pandas.pivot_table(self.stateAndCessation, index=['YEAR','LocationAbbr'], columns=['MeasureDesc'] , values='Data_Value')
       
        
    def analyzeCigaretteUse(self):
        self.stateAndCigaretteUse=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cigarette Use (Youth)' )][['YEAR','LocationAbbr','MeasureDesc','Response','Data_Value']]
        self.stateAndCigaretteUse['CigaretteUseStatus'] = self.stateAndCigaretteUse[['MeasureDesc', 'Response']].apply(lambda x: ' '.join(x), axis=1)
        
        self.stateAndCigaretteUse=self.stateAndCigaretteUse.groupby(['YEAR','LocationAbbr','CigaretteUseStatus'], as_index=False)['Data_Value'].mean()
        self.stateAndCigaretteUse=self.stateAndCigaretteUse.sort_values(by=['YEAR','LocationAbbr'], ascending=False)
        self.stateAndCigaretteUse=pandas.pivot_table(self.stateAndCigaretteUse, index=['YEAR','LocationAbbr'], columns=['CigaretteUseStatus'] , values='Data_Value')
       
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

    def plotBeforeAndAfterCampaign(self):
        '''
        self.stateCigaretteUseResult.plot(figsize=(20,20),
                                   style = '--o',
                                   title = "Cigarette Use by State ")
                                   '''
        pandas.DataFrame.hist(self.stateCigaretteUseResult)

        




