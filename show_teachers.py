"""
show_teachers.py
created: 17/04/21
methods to display visualiations for dataframes
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

'''
graph teachers - pass in teachers dataframe with teacher statistics
'''

# use pink/blue to make it easy to identify genders
gender_colors = ["#FC46AA", "#00BFFF"]

def show_career_breaks(careers, totals):
    all_teachers = careers.merge(totals, on="Year", suffixes=("_cb", "_tot"))
    all_teachers['All_CB'] = all_teachers['Male_CB'] + all_teachers['Female_CB']
    show_gender_percentages("Primary teachers' career breaks by gender", all_teachers, "Male_CB", "Female_CB", "All")


def show_principals(all_teachers):
    print(all_teachers.head(1))
    all_teachers["All_Prin"] = all_teachers['Male_Prin'] + all_teachers['Female_Prin']
    show_gender_percentages("Primary teachers by gender", all_teachers, "Male_All", "Female_All", "All")
    show_gender_percentages("Primary principals by gender", all_teachers, "Male_Prin", "Female_Prin", "All_Prin")


def show_gender_percentages(title, totals, male_col, female_col, total_col):
    # calculate 2 extra cols for percentage of male and female
    p1 = 'Female'
    p2 = 'Male'
    totals[p1] = totals[female_col] / totals[total_col] * 100
    totals[p2] = totals[male_col] / totals[total_col] * 100

    # create new dataframe with just the Year and percentages cols
    percents = totals.loc[:, ['Year', p1, p2]]
    # melt to tall dataframe
    percents = percents.melt(id_vars=['Year'], var_name='Gender', value_name='percent')

    # show on a simple grouped bar plot
    p = sns.catplot(kind='bar', data=percents, x='Year', y='percent', hue="Gender", palette=gender_colors)
    p.set_axis_labels("School Year", "Percentages")
    plt.title(title)

    # show same scale for all
    plt.yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
               ["", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"])
    # Show plot
    p.savefig("images\\%s" % title)
    plt.show()


def show_teacher_population(totals):
    p = sns.lineplot(data=totals, x='Full_Year', y='All')

    p.set(xlabel='School Year', ylabel='Number of teachers')
    plt.title("Teacher Population by year")
    plt.show()


def show_gender_pie(all_teachers):
    # Pie chart will work best for 1 year of data
    all_teachers = all_teachers.set_index("Full_Year")

    # get data for the teacher pie chart - 2017 row with cols for male/female TEACHERS
    t = all_teachers.loc[["2017/2018"], ["Female_All", "Male_All"]]
    # get data frame into format for pie chart by pivoting it and renaming cols
    t.rename(columns={"Female_All": "Female", "Male_All": "Male"}, inplace=True)
    t = t.melt().set_index("variable")

    # get dataframe for the principal pie chart - 2017 row with cols for male/female PRINCIPALS
    p = all_teachers.loc[["2017/2018"], ["Female_Prin", "Male_Prin"]]
    # get data frame into format for pie chart by pivoting it and renaming cols
    p.rename(columns={"Female_Prin": "Female", "Male_Prin": "Male"}, inplace=True)
    p = p.melt().set_index("variable")


    # set up 2 plots on the figure to compare pie charts side by side
    fig, ax = plt.subplots(1, 2)
    t.plot(kind='pie', y="value", ylabel="", colors=gender_colors, title="Teachers", ax=ax[0], autopct='%1.1f%%', startangle=0,
           fontsize=12, legend=False)
    p.plot(kind='pie', y="value", ylabel="", colors=gender_colors, title="Principals", ax=ax[1], autopct='%1.1f%%',
           startangle=0, fontsize=12, legend=False)

    # Add an overall title
    title = "2017 Primary school staff by gender"
    fig.suptitle(title)
    fig.savefig("images\\%s" % title)
    plt.show()
