
import pandas
import numpy
import matplotlib 
import datetime
from YouthSmokingAnalysis import YouthSmokingAnalysis 

class CampaignAnalysis(YouthSmokingAnalysis):
    
    def __init__(self):
        YouthSmokingAnalysis.__init__(self)
    def analyzeGender(self):
        yearandGenderGroup=self.ytsDataFrame[(self.ytsDataFrame.Gender!='Overall')
                                             & (self.ytsDataFrame.TopicDesc=='Cigarette Use (Youth)' )
                                             & (self.ytsDataFrame.MeasureDesc=='Smoking Status') & (self.ytsDataFrame.Response=='Ever')]
        yearandGenderGroup["NumberOfPeople"]=(yearandGenderGroup.Data_Value*yearandGenderGroup.Sample_Size)/100
        print(yearandGenderGroup[['YEAR','Gender','Data_Value','Sample_Size','NumberOfPeople']])
        numberOfPeopleSmoking=yearandGenderGroup.groupby(['YEAR','Gender'])['NumberOfPeople'].sum()
        numberOfPeopleSmoking.plot()
        print(yearandGenderGroup.groupby(['YEAR','Gender'])['NumberOfPeople'].sum())


a=CampaignAnalysis()
a.analyzeGender()
