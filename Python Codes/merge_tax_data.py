import string
"""
this program merges the tax rate data into a single csv file for use in analyses
author: Tony santos, group 4
"""
from os.path import join, dirname, abspath
import os
import xlrd


def is_merged(sheet, row, column):
    """
    :param sheet: handle to excel worksheet
    :param row: row index of cell to check
    :param column: column index of cell to check
    :return: tuple with 2 values; boolean of whether cell is merged and bottom row of cell whether merged or not
    this code adapted from code found on stackexchange:
        http://stackoverflow.com/questions/37419699/end-of-merged-cells-in-excel-with-python
    original only returned false if the cell was not a merged cell. this version returns original row index
    if cell is not merged
    this was needed because early years had merged cells and later years did not
    """
    for cell_range in sheet.merged_cells:
        row_low, row_high, column_low, column_high = cell_range
        if row in range(row_low, row_high) and column in range(column_low, column_high):
            return (True, row_high-1)
    return (False, row)

def clean_state(state):
    """
    :param state: string contianing the text found in the state name column
    :return:  returns a cleaned up version of the state entry with any footnote numbers removed, and abbreviations
            replaced with the proper name
    """

    reformatted_state = state
    # 1st, remove any footnotes from end of entry
    if '(' in state:
        reformatted_state = state[:state.index('(', 0)].strip()  # remove any trailing spaces remaining after parens deleted

    # replace abbreviations
    if reformatted_state == 'D.C.':
        reformatted_state = 'District of Columbia'
    elif reformatted_state[0:2] == 'N.':
        reformatted_state = 'North' + reformatted_state[2:]
    elif reformatted_state[0:2] == 'S.':
        reformatted_state = 'South' + reformatted_state[2:]
    elif reformatted_state[0:2] == 'W.':
        reformatted_state = 'West' + reformatted_state[2:]
    elif reformatted_state == 'Penn.':
        reformatted_state = 'Pennsylvania'

    return reformatted_state


dirpath = os.getcwd()
# dirpath = "C:\\Python for Data Science\\FinalProject"
file_name = "State Sales, Gasoline, Cigarette and Alcohol Taxes, 2000-2014.xlsx"
fname = join(dirpath, file_name)
tax_data = []

# Open the workbook
xl_workbook = xlrd.open_workbook(fname)
# List sheet names, and pull a sheet by name
#
sheet_names = xl_workbook.sheet_names()
sheet_names.sort()
print('Sheet Names', sheet_names)
for sheet_name in sheet_names:
    xl_sheet = xl_workbook.sheet_by_name(sheet_name)
    year = xl_sheet.name

    """
    skip rows until "cigarette tax" is found in column 3 (D)
    after finding "cigarette tax", check for merged cells to determine 1st data row
    """

    row_index = 0
    while row_index < xl_sheet.utter_max_rows:
        cell = xl_sheet.cell(row_index, 3)
        found_it = 'cigarette tax' in str(cell.value).lower()
        if found_it:
            # header row is current row index
            header_row_index = row_index
            # 1st data row: add 1 to last row of merged cell (2nd value returned from is_merged)
            data_start_row = is_merged(xl_sheet, row_index, 3)[1] + 1
            row_index = is_merged(xl_sheet, row_index, 3)[1]
            break
        row_index += 1
    if row_index >= xl_sheet.utter_max_rows:
        print("ERROR: cigarette tax data not found")
        exit(11)
    # read in state name and cigarette tax rate for 50 state and Ditrict of Columbia (D.C.)
    # when you get to Wyoming, if next row had district of columbia or D.C., ad it to list, otherwise, it is the
    #  end of data rows
    # District of columbia and D.C. should get mapped to the same entry for each year

    for row_index in range(data_start_row, data_start_row + 51):
        year = xl_sheet.name
        state = xl_sheet.cell(row_index, 0).value.strip()
        state = clean_state(state)
        tax_rate = str(xl_sheet.cell(row_index, 3).value)

        tax_rate = ''.join(
            [str(ch) for ch in tax_rate if ch in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']])
        if year in ['2000', '2001', '2002', '2003', '2004']:
            tax_rate = round(float(tax_rate), 2)
        else:   #taxes in dollars
            tax_rate = round(float(tax_rate) * 100, 4)

        tax_data.append((year, state, tax_rate))

with open("tax_data_all.csv", "w") as fo:
    fo.write("YEAR,STATE,TAX RATE\n")
    fo.write('\n'.join('"{}","{}",{}'.format(x[0], x[1], x[2]) for x in tax_data))
    # fo.write('\n'.join('{},{},{}'.format(x[0], x[1], x[2]) for x in tax_data))

