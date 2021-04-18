"""
webscrape.py
created: 17/04/21
example code to read info from web site into a dataframe and analyse

"""
import requests
import pandas as pd
from bs4 import BeautifulSoup


def do_webscrape():
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

    print('Carrers', career_breaks.head())
    print('totals', total_teachers.head())
    print('jobshare', jobsharing.head())
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
                data.append([int(x) if x.isdigit() else x for x in this_row ])
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
    headers = ["Year", "Male_CB", "Female_CB"]
    new_careers = new_careers.set_axis(headers, axis=1)
    # print(new_careers.head())

    # Totals - Need to use first row of data as the headers
    headers = ['Year', 'Female_All', 'Male_All','Female_Prin', 'Male_Prin', 'All']
    new_totals = raw_totals.iloc[1:, 0:6]
    new_totals = new_totals.set_axis(headers, axis=1)
    # new_totals rename(columns={"\xa0":"School Year"}, inplace=True)
    # print(new_totals.head(10))

    # Job Sharing
    # just need first 2 cols
    new_jobsharing = raw_jobsharing.iloc[:, 0:2]
    # Tidy up headers
    headers = ["Year", "All_JS"]
    new_jobsharing = new_jobsharing.set_axis(headers, axis=1)

    return new_careers, new_jobsharing, new_totals


