
import pandas
import numpy
import matplotlib 
import datetime
from YouthSmokingAnalysis import YouthSmokingAnalysis

class EducationAnalysis(YouthSmokingAnalysis):
    
    def __init__(self):
        YouthSmokingAnalysis.__init__(self)
    def analyze(self):
        #'Middle School' 'High School'
        yearandEducationGroup=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cigarette Use (Youth)' )
                                             & (self.ytsDataFrame.MeasureDesc=='Smoking Status')
                                             & (self.ytsDataFrame.Response=='Ever')]
        yearandEducationGroup["NumberOfPeople"]=(yearandEducationGroup.Data_Value*yearandEducationGroup.Sample_Size)/100
        print(yearandEducationGroup[['YEAR','Education','Data_Value','Sample_Size','NumberOfPeople']])
        numberOfPeopleSmoking=yearandEducationGroup.groupby(['YEAR','Education'])['NumberOfPeople'].sum()
        print(yearandEducationGroup.groupby(['YEAR','Education'])['NumberOfPeople'].sum())
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
        
a=EducationAnalysis()
a.analyze()
