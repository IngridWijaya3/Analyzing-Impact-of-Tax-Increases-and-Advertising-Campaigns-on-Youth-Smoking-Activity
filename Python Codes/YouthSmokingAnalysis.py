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
        #self.clean_YTS_dataset(YouthSmokingAnalysis.ytsOriginalFile,YouthSmokingAnalysis.ytsCsvFileName)
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
    
    def clean_YTS_dataset(self,input_file, output_file):
        # Read the CSV, Clean the data, Write to output file
        
        # input_file - '.csv' file that needs to be cleaned
        # output_file - desired name of the cleaned csv file
        
        # The only cleaning that needs to be done corresponds to the Data_Value_Footnote column
        # where the value is 'Data in these cells have been suppressed because of a small sample size'


        # Read in the csv into a Pandas dataframe (dfMAIN)
        dfMAIN = pandas.read_csv(input_file)

        # Check the shape of the dataset
        print('** Shape of the original dataset ', dfMAIN.shape)
     
        # Check how many rows contain 'Data in these cells have been suppressed because of a small sample size' in the Data_Value_Footnote column
        print(dfMAIN.Data_Value_Footnote.value_counts())

        # Delete the rows where the column Data_Value_Footnote == 'Data in these cells have been suppressed because of a small sample size'
        dfMAIN = dfMAIN[dfMAIN.Data_Value_Footnote != 'Data in these cells have been suppressed because of a small sample size']

        # Check shape of the new dataset
        print('** Shape of the clean dataset ', dfMAIN.shape)

        # Write to CSV file with the name of 'output_file'. Index is set to False as we do not want the Pandas Index in our output file
        dfMAIN.to_csv(output_file, index=False, encoding='utf-8')
        
        print("Output file is %s" %output_file)



