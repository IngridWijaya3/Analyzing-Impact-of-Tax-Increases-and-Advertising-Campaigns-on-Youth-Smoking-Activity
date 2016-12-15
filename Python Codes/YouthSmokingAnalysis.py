import pandas
import numpy
import matplotlib 
import datetime

class YouthSmokingAnalysis:
    csvFileName="YTS_Clean.csv"
    taxRateCsvFileName="tax_data_all.csv"
    outputCSVFolderName= "AnalysisCSV"
    outputPlotFolderName="Plots"
    def __init__(self):
        self.ytsDataFrame= pandas.read_csv("YTS_Clean.csv")
        self.taxRateDataFrame= pandas.read_csv("tax_data_all.csv")
        self.YTSAndTaxRateDataFrame=pandas.merge( self.ytsDataFrame, self.taxRateDataFrame, left_on=['YEAR','LocationDesc'], right_on=['YEAR','STATE'])
        print(self.YTSAndTaxRateDataFrame)
    def analyze(self):
        pass
    def analyzeCessation(self):
        pass
    def analyzeNonCessation(self):
        pass
    def analyzeBeforeAndAfterCampaign(self):
        pass
    def analyzeBeforeAndAfterTax(self):
        pass
    def plotResult(self):
        pass


a=YouthSmokingAnalysis()


