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
    missing_val = pupils.isnull()
    missing_val = pupils.isna()  # SAME!
    return pupils


# print(missing_val.isna().any())


# print(missing_val)	# this is matching data from with True for all null values
# print(missing_val.sum())
'''
# PLOT THE NUMBER OF MISSING VALUES FOR EACH COLUM!
pupils.isna().sum().plot(kind="bar")
plt.show()

pupils = pupils.fillna(pupils.mean)
pupils.isna().sum().plot(kind="bar")
plt.show()
'''

def clean_pupil_data(pupils):
    # need to CLEAn DAta to remove the summary rows that are in there
    # Delete these row indexes from dataFrame
    # df.drop(indexNames , inplace=True)
    print('BEFORE pupils clean')
    show_unique_values(pupils, 'Age')
    show_unique_values(pupils, 'School Programme')

    # drop the rows that contain 'All ages'
    drop = pupils[pupils['Age'] == 'All ages'].index
    pupils.drop(drop, inplace=True)

    # drop the rows that contain summary info for classes
    summary_classes = ['All mainstream national school programmes',
                    'All first level school programmes',
                    'All first level education institutions aided by the Department of Education and Skills']
    for v in summary_classes:
        pupils['cat'] = np.where(pupils['School Programme'] == v, 'All', 'Single')
        drop = pupils[pupils['cat'] == 'All'].index
        pupils.drop(drop, inplace=True)

    print('AFTER pupils clean')
    show_unique_values(pupils, 'Age')
    show_unique_values(pupils, 'School Programme')
    return pupils

# show the unique values in a column
def show_unique_values(df, colname):
    values = df[colname].unique()
    print('There are %d unique <%s> values: ' % (len(values), colname))
    print(values)