
import pandas
import numpy
import matplotlib 
import datetime
from YouthSmokingAnalysis2 import YouthSmokingAnalysis2
class StateAnalysis(YouthSmokingAnalysis2):
    
    def __init__(self):
        YouthSmokingAnalysis2.__init__(self)
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

a=StateAnalysis()
a.analyze()

