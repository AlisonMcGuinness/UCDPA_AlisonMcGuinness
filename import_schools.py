"""
import_schools.py
created: 18/04/2021

for importing individual schools data from XLS file on web to dataframe
"""

from urllib.request import urlretrieve

# Import pandas
import pandas as pd
import numpy as np

def get_schools_data():

    all_schools_file = "data\\primary-schools-2020-2021.xlsx"
    xls = pd.ExcelFile(all_schools_file)
    school_types = xls.parse(1, usecols=[1, 12], skiprows=1)

    # calculate urban or rural based on Local Authority
    school_types["type"] = np.where(school_types["Local Authority Description"].str.contains("City Council"), "Urban", "Rural")
    school_types = school_types.drop("Local Authority Description", axis=1)
    print(school_types.head())

    class_sizes_file  = "data\\class-size-2019-2020.xlsx"
    sheet_name = "2 Individual Class Data"
    # Read in all sheets of Excel file: xls
    xls = pd.ExcelFile(class_sizes_file)
    # Load the third sheet into a DataFrame by index: all_data

    # we only need the column with the school roll number (0)
    # and all the cols from Class 1 to Class 40
    keep_cols = [x for x in range(8,48)]
    keep_cols.append(0)
    all_data = xls.parse(2, usecols=keep_cols, skiprows=3)

    # There is typo in the file - the first col is actually the roll number so rename it
    all_data.rename(columns={"Academic Year": "Roll Number"}, inplace=True)
    print(all_data.head())
    # unpivot the data to long format to make it easier to graph

    all_data = all_data.melt(id_vars="Roll Number")
    # Print the head of the DataFrame df2
    print(all_data.shape)
    print(all_data.head())

    # remove all the blank rows
    all_data = all_data.dropna(axis=0, how="any")
    print(all_data.shape)
    print(all_data.head())
    print('customising import  - skip rows, select columns, rename ')
    print('these are all parameters to PARSE')

    print(all_data.head())


    all_schools = all_data.merge(school_types, how="left", on="Roll Number")
    print(all_schools.head())
    return all_schools