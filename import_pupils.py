"""
import_pupils.py
created: 18/04/2021

functions to read pupil statisics from csv file into a dataframe and clean the data

"""
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)


# function to read data from csv file to pandas dataframe
def get_pupil_data():
    # data file downloaded from
    pupils = pd.read_csv('data\\EDA42.20210405T120415.csv')
    print('Pupils')
    print(pupils.head(5))
    print(pupils.shape)
    return pupils


def clean_pupil_data(pupils):
    # need to clean data to remove the summary rows that are in there
    # Delete these row indexes from dataFrame
    # df.drop(indexNames , inplace=True)
    print('BEFORE pupils clean')
    show_unique_values(pupils, 'Age')
    show_unique_values(pupils, 'School Programme')

    # drop the rows that contain 'All ages'
    drop = pupils[pupils['Age'] == 'All ages'].index
    pupils.drop(drop, inplace=True)

    # drop the rows that contain summary info for classes as this is duplicate info
    drop_programmes = ['All mainstream national school programmes',
                       'All first level school programmes',
                       'All first level education institutions aided by the Department of Education and Skills']
    for drop_value in drop_programmes:
        # create a new column that is set to "All" for all rows to be dropped
        pupils['cat'] = np.where(pupils['School Programme'] == drop_value, 'All', 'Single')
        # drop all the rows that are set to "All"
        drop = pupils[pupils['cat'] == 'All'].index
        pupils.drop(drop, inplace=True)

    print('AFTER pupils clean')
    show_unique_values(pupils, 'Age')
    show_unique_values(pupils, 'School Programme')
    return pupils


# show the unique values in a column - for debugging/verification
def show_unique_values(df, col_name):
    values = df[col_name].unique()
    print('There are %d unique <%s> values: ' % (len(values), col_name))
    print(values)
