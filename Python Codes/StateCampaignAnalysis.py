
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
        self.plotBeforeAndAfterCampaign()
        
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

        plt.style.use('fivethirtyeight')

        #plt.draw_all()

        #plt.savefig('test.png')

        n_groups = len(self.stateCigaretteUseResult.index)

        means_men = self.stateCigaretteUseResult["AverageBeforeCampaign"].values
        means_women = self.stateCigaretteUseResult["AverageAfterCampaign"].values

        fig, ax = plt.subplots()
        fig.set_figheight(20)
        fig.set_figwidth(30)
        
        index = numpy.arange(n_groups)
        index = numpy.arange(0, n_groups * 2, 2)
        bar_width = 0.35

        opacity = 0.4
        error_config = {'ecolor': '0.3'}

        rects1 = plt.bar(index, means_men, bar_width,
                     alpha=opacity,
                     color='b',
                     error_kw=error_config,
                     label='Before Campaign')

        rects2 = plt.bar(index + bar_width, means_women, bar_width,
                     alpha=opacity,
                     color='r',
                     error_kw=error_config,
                     label='After Campaign')

        plt.xlabel('States')
        plt.ylabel('Percent Average')
        plt.title('Percent Average Cigarette Use Before And After Campaign')
        plt.xticks(index + bar_width, self.stateCigaretteUseResult.index,fontsize=10)
       
        plt.legend()

        #plt.show()
        plt.savefig('test.png')

a = StateCampaignAnalysis()
a.analyze()

        




