
import pandas
import numpy
import matplotlib 
import datetime
from YouthSmokingAnalysis2 import YouthSmokingAnalysis2

class EducationAnalysis(YouthSmokingAnalysis2):
    
    def __init__(self):
        YouthSmokingAnalysis2.__init__(self)
    def analyze(self):
        #'Middle School' 'High School'
        yearandEducationGroup=self.ytsDataFrame[(self.ytsDataFrame.Gender=='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cigarette Use (Youth)' )
                                             & (self.ytsDataFrame.MeasureDesc=='Smoking Status')
                                             & (self.ytsDataFrame.Response=='Ever')]
        yearandEducationGroup["NumberOfPeople"]=(yearandEducationGroup.Data_Value*yearandEducationGroup.Sample_Size)/100
        print(yearandEducationGroup[['YEAR','Education','Data_Value','Sample_Size','NumberOfPeople']])
        numberOfPeopleSmoking=yearandEducationGroup.groupby(['YEAR','Education'])['NumberOfPeople'].sum()
        numberOfPeopleSmoking.plot()
        print(yearandEducationGroup.groupby(['YEAR','Education'])['NumberOfPeople'].sum())

a=EducationAnalysis()
a.analyze()
