"""
import_teachers.py
created: 17/04/21

functions to read teacher statisics from web site into a dataframe and clean the data

"""
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_teacher_data():
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', 2000)

    # For this example use webpage published by education.id with that has Teacher Statistics
    url = "https://www.education.ie/en/Publications/Statistics/teacher-statistics/"
    # These are the html headers on the page for the data tables that we want to inspect
    careers_table = "Breakdown of Career Break by year, sector and gender for 2012/2013 - 2018/2019"
    total_table = "Number of teachers by gender appointed to teaching posts"
    jobshare_table = "Number of Teachers that are job-sharing"

    # Use requests.get to get HTMl from url
    r = requests.get(url)
    html = r.text

    # Create a BeautifulSoup object from the HTML: soup
    soup = BeautifulSoup(html)

    # load up the data from the html into DataFrames for each table
    career_breaks = read_table(soup, careers_table)
    jobsharing = read_table(soup, jobshare_table)
    total_teachers = read_table(soup, total_table)

    print('Career Breaks (raw)')
    print(career_breaks.head())
    print('Total teachers (raw)')
    print(total_teachers.head())
    print('Job Sharing (raw)')
    print(jobsharing.head())

    return career_breaks, jobsharing, total_teachers


# function to read from soup  - find the '<table>' after the given header and return it in a DataFrame
def read_table(soup, table_head):
    df = None
    table = soup.find(text=table_head).findNext('table')

    # iterate through the table items and make a list of lists
    for table_body in table.children:
        first = True
        cols = []  # for the dataframe column headers
        data = []  # actual data
        for tr in table_body.children:  # each row of the table
            this_row = []
            for td in tr.children:
                # make a list of the items in this row
                colspan = int(td.attrs.get('colspan', 1))
                add_td(this_row, td.text, colspan)

            if first:
                # if this is the first row then use it as the column headers
                cols = this_row
                first = False
            else:
                # all other rows should be integer values
                data.append([int(x) if x.isdigit() else x for x in this_row])
        # convert lists of data to a DataFrame
        df = pd.DataFrame(data, columns=cols)
    return df


def add_td(row, data, colspan):
    for count in range(colspan):
        row.append(data)


# Tidy up the Raw data from webscraping
def tidy_teacher_data(raw_careers, raw_jobsharing, raw_totals):
    # Make sure each DataFrame has a Year column so we can merge

    # Career Breaks
    # Just want first 3 columns
    new_careers = raw_careers.iloc[:, 0:3]
    # Tidy up headers
    headers = ["Full_Year", "Male_CB", "Female_CB"]
    new_careers = new_careers.set_axis(headers, axis=1)
    new_careers = fix_year_col(new_careers, "Full_Year", "Year")
    # print(new_careers.head())

    # Totals - Need to use first row of data as the headers
    headers = ["Full_Year", "Female_All", "Male_All", "Female_Prin", "Male_Prin", "All"]

    new_totals = raw_totals.iloc[1:, 0:6]
    new_totals = new_totals.set_axis(headers, axis=1)
    new_totals = fix_year_col(new_totals, "Full_Year", "Year")
    new_totals = new_totals.infer_objects().sort_values('Year', ascending=True)

    # Job Sharing
    # just need first 2 cols
    new_jobsharing = raw_jobsharing.iloc[:, 0:2]
    # Tidy up headers
    headers = ["Full_Year", "All_JS"]
    new_jobsharing = new_jobsharing.set_axis(headers, axis=1).infer_objects()
    new_jobsharing = fix_year_col(new_jobsharing, "Full_Year", "Year")
    print(new_jobsharing)
    new_jobsharing = new_jobsharing.sort_values("Year", ascending=True)

    print("Career Breaks (clean)")
    print(new_careers.head())
    print("Total teachers (clean)")
    print(new_totals.head())
    print("Job Sharing (clean)")
    print(new_jobsharing.head())
    return new_careers, new_jobsharing, new_totals


# create new column on the df called <new_col> taking value from the first year in old_col in format year/year
# drop any rows where the year col is not an integer first
def fix_year_col(df, year_col, new_col):
    df[new_col] = df[year_col].str.split('/').str[0]
    ok_rows = df[df[new_col].str.isdigit()]
    return ok_rows.astype({new_col: int})
