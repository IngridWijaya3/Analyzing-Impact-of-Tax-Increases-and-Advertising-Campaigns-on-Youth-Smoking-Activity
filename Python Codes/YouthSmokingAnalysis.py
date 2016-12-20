import pandas
import numpy
import matplotlib 
import datetime

class YouthSmokingAnalysis:
    ytsCsvFileName="YTS_Clean.csv"
    taxRateCsvFileName="tax_data_all_cleaned.csv"
    outputCSVFolderName= "AnalysisCSV"
    outputPlotFolderName="Plots"
    ytsOriginalFile="Youth_Tobacco_Survey__YTS__Data.csv"
    
    def __init__(self):
        self.ytsDataFrame= pandas.read_csv(YouthSmokingAnalysis.ytsCsvFileName)
        self.taxRateDataFrame= pandas.read_csv(YouthSmokingAnalysis.taxRateCsvFileName)
        self.YTSAndTaxRateDataFrame=pandas.merge( self.ytsDataFrame, self.taxRateDataFrame, left_on=['YEAR','LocationDesc'], right_on=['YEAR','STATE'])
        
    def analyze(self):
        pass
    def analyzeCessation(self):
        pass
    def analyzeCigaretteUse(self):
        pass
    def analyzeBeforeAndAfterCampaign(self):
        pass
    def analyzeBeforeAndAfterTax(self):
        pass
    def plotResult(self):
        pass
    
 

