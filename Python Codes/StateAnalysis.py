
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
                                             & (self.ytsDataFrame.MeasureDesc=='Smoking Status')
                                             & (self.ytsDataFrame.Response=='Ever')]
        yearandStateGroup["NumberOfPeople"]=(yearandStateGroup.Data_Value*yearandStateGroup.Sample_Size)/100
        print(yearandStateGroup[['YEAR','LocationAbbr','Data_Value','Sample_Size','NumberOfPeople']])
        numberOfPeopleSmoking=yearandStateGroup.groupby(['YEAR','LocationAbbr'], as_index=False)['NumberOfPeople'].sum()
        pivotTable=pandas.pivot_table(numberOfPeopleSmoking, index=['YEAR'], columns=['LocationAbbr'] , values='NumberOfPeople')


        print(numberOfPeopleSmoking)
        print(pivotTable)
        return numberOfPeopleSmoking
    def analyzeCessation(self):
        print("add codes here")
    def analyzeNonCessation(self):
        print("add codes here")
    def analyzeBeforeAndAfterCampaign(self):
        print("add codes here")
    def analyzeBeforeAndAfterTax(self):
        print("add codes here")
    def plotResult(self):
        print("add codes here")

a=StateAnalysis()
a.analyze()

