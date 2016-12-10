
import pandas
import numpy
import matplotlib 
import datetime
from YouthSmokingAnalysis import YouthSmokingAnalysis
class GenderAnalysis(YouthSmokingAnalysis):
    
    def __init__(self):
        YouthSmokingAnalysis.__init__(self)
    def analyze(self):
        yearandGenderGroup=self.ytsDataFrame[(self.ytsDataFrame.Gender!='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cigarette Use (Youth)' )
                                             & (self.ytsDataFrame.MeasureDesc=='Smoking Status') & (self.ytsDataFrame.Response=='Ever')]
        yearandGenderGroup["NumberOfPeople"]=(yearandGenderGroup.Data_Value*yearandGenderGroup.Sample_Size)/100
        print(yearandGenderGroup[['YEAR','Gender','Data_Value','Sample_Size','NumberOfPeople']])
        numberOfPeopleSmoking=yearandGenderGroup.groupby(['YEAR','Gender'], as_index=False)['NumberOfPeople'].sum()
        pivotTable=pandas.pivot_table(numberOfPeopleSmoking, index=['YEAR'], columns=['Gender'] , values='NumberOfPeople')


        print(numberOfPeopleSmoking)
        print(pivotTable)
        
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
        
a=GenderAnalysis()
a.analyze()

