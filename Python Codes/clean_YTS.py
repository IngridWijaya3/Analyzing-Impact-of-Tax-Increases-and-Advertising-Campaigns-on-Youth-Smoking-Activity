import pandas as pd

def clean_YTS_dataset(input_file, output_file):

    # Read the CSV, Clean the data, Write to output file
    
    # input_file - '.csv' file that needs to be cleaned
    # output_file - desired name of the cleaned csv file
    
    # The only cleaning that needs to be done corresponds to the Data_Value_Footnote column
    # where the value is 'Data in these cells have been suppressed because of a small sample size'


    # Read in the csv into a Pandas dataframe (dfMAIN)
    dfMAIN = pd.read_csv(input_file)

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


###clean_YTS_dataset('../Youth_Tobacco_Survey__YTS__Data.csv','YTS_Clean.csv')
