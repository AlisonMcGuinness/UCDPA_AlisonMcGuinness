"""
import_schools.py
created: 18/04/2021

for importing individual schools data from XLS file on web to dataframe
"""
from counties import county_lookup
import pandas as pd
import numpy as np

"""
There is a separate file for each year online
These have mostly the same format but some slight differences each year
The differences are
"roll" - the column that holds the school roll number
"start" - the first column that holds class size info
"cols" - how many class size cols there are in the file
"skip" - how many rows at the top of the file have to be skipped
"""
school_years = {
    #2019: {"roll": 0, "start": 8, "cols": 40, "skip": 3},
    #2018: {"roll": 0, "start": 8, "cols": 40, "skip": 3},
    #2017: {"roll": 0, "start": 8, "cols": 39, "skip": 3},
    #2016: {"roll": 0, "start": 8, "cols": 39, "skip": 3},
    #2015: {"roll": 1, "start": 5, "cols": 37, "skip": 4},
    #2014: {"roll": 1, "start": 5, "cols": 37, "skip": 4, "sheet": "2. Individual Class Data", "format": "xls"},
    #2013: {"roll": 1, "start": 5, "cols": 36, "skip": 4, "format": "xls"},
    #2012: {"roll": 1, "start": 5, "cols": 35, "skip": 4, "format": "xls"},
    #2011: {"roll": 1, "start": 5, "cols": 35, "skip": 4, "sheet": "2. Individual class data", "format": "xls", "file_name": "Class%20Size%20"},
    2010: {"roll": 1, "start": 5, "cols": 35, "skip": 4, "sheet": "2. Individual class data", "format": "xls", "file_name": "Class%20Size%20"}
}


def get_schools_data():
    # there is a file of class sizes for each year
    # concatenate them all together
    # get a list of all schools and their counties
    school_types = get_school_info()
    all_years = None
    for year, year_info in school_years.items():
        year = get_classes_by_year(school_types, year, year_info)
        if all_years is None:
            all_years = year
        else:
            all_years = pd.concat([all_years, year])
    print('bfore merge', all_years.shape)
    print(all_years.head())
    all_schools = all_years.merge(school_types, on="Roll Number")
    print('after merge', all_schools.shape)
    print(all_schools.head())

    avgs = all_schools.groupby(['year', 'Province'])['value'].mean()

    print('sum')
    print(all_schools.groupby(['year', 'Province'])['value'].sum())
    print('counts')
    print(all_schools.groupby(['year', 'Province'])['value'].count())

    print('all leinster', all_schools[all_schools['Province']=="Leinster"].count())
    print(avgs.head(40))
    return all_schools


def get_classes_by_year(schools, year, year_info):
    url = "https://www.education.ie/en/Publications/Statistics/Data-on-Individual-Schools/primary/class-size/"
    file_name = "%s%d-%d.%s" % (year_info.get("file_name", "class-size-"), year, year + 1, year_info.get("format", "xlsx"))

    # class sizes are on the 3rd sheet in the file
    sheet_name = year_info.get("sheet", "2 Individual Class Data")
    # class_sizes_file  = "data\\class-size-2019-2020.xlsx"

    # Read in all sheets of Excel file: xls
    # xls = pd.ExcelFile(class_sizes_file)
    # Load the third sheet into a DataFrame by index: all_data

    # we only need the column with the school roll number (0)
    # and all the cols from Class 1 to Class 40
    keep_cols = [x for x in range(year_info["start"], year_info["start"] + year_info["cols"])]
    keep_cols.append(year_info["roll"])
    # all_data = xls.parse(2, usecols=keep_cols, skiprows=3)
    print(url + file_name)
    all_data = pd.read_excel(url + file_name, sheet_name=sheet_name, skiprows=range(0, year_info["skip"]),
                             usecols=keep_cols)

    # One file has a typo - the roll number is lablelled 'acdemic year'  so rename it
    all_data.rename(columns={"Academic Year": "Roll Number"}, inplace=True)
    # Some files have a different label for the roll no col so rename it
    all_data.rename(columns={"Roll No": "Roll Number"}, inplace=True)
    all_data.rename(columns={"RollNo": "Roll Number"}, inplace=True)

    print(all_data.head())
    print(all_data.shape)

    # unpivot the data to long format to make it easier to graph
    all_data = all_data.melt(id_vars="Roll Number")
    # Print the head of the DataFrame df2
    print(all_data.shape)
    print(all_data.head())

    # remove all the blank rows
    all_data = all_data.dropna(axis=0, how="any")
    all_data = all_data.drop("variable", axis=1)
    # add year col
    all_data['year'] = year
    print(all_data.shape)
    print(all_data.head())
    print('customising import  - skip rows, select columns, rename ')
    print('these are all parameters to PARSE')
    print(all_data.head())
    print(all_data['value'].sum())
    print(all_data['value'].count())
    return all_data

# get a dataframe with all schools roll numbers and PROVINCE
# schools don't change much year to year so get one set from 10 years ago
# and one from now and merge them together, removing duplicates to get one master list
def get_school_info():
    all_schools_file = "data\\primary-schools-2020-2021.xlsx"
    xls = pd.ExcelFile(all_schools_file)

    # just get a list of roll number and county
    school_types = xls.parse(1, usecols=[1, 7], skiprows=1)
    print(school_types.head(), school_types.shape)

    old_schools_file = "data\\Primary Schools 2011-2012.xls"
    xls = pd.ExcelFile(old_schools_file)
    old_types = xls.parse(0, usecols=[0, 2], skiprows=2)
    old_types.rename(columns={"County Name":"County Description", "Roll No.":"Roll Number"}, inplace=True)
    print(old_types.head(), old_types.shape)

    school_types = pd.concat([school_types, old_types])
    print(school_types.head(), school_types.shape)

    #remove duplicates
    school_types = school_types.drop_duplicates()
    print(school_types.head(), school_types.shape)


    # calculate province based on the county using the county_lookup
    school_types["Province"] = school_types['County Description'].apply(get_province)
    school_types = school_types.drop("County Description", axis=1)
    print(school_types.head())

    return school_types


def get_province(county_code):
    return county_lookup.get(county_code, '')


"""
def get_school_info():

    all_schools_file = "data\\primary-schools-2020-2021.xlsx"
    xls = pd.ExcelFile(all_schools_file)

    # just get a list of roll number and Local authority
    school_types = xls.parse(1, usecols=[1, 12], skiprows=1)

    # calculate urban or rural based on Local Authority
    school_types["type"] = np.where(school_types["Local Authority Description"].str.contains("City Council"), "Urban", "Rural")
    school_types = school_types.drop("Local Authority Description", axis=1)
    print(school_types.head())

    return school_types
"""
