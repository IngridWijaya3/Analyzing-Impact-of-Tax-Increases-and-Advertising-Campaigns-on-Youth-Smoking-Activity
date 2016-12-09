import pandas
import numpy
import matplotlib 
import datetime

class YouthSmokingAnalysis:
    csvFileName="YTS_Clean.csv"
    def __init__(self):
        self.ytsDataFrame= pandas.read_csv("YTS_Clean.csv")
   
    def analyzeGender(self):
        pass
    def analyzeEducation(self):
        pass
    def analyzeState(self):
        pass        


a=YouthSmokingAnalysis()
