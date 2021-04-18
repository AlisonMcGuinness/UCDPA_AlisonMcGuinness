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
def show_career_breaks(careers, totals):
    all_teachers = careers.merge(totals, on="Year", suffixes=("_cb", "_tot"))
    all_teachers['All_CB'] = all_teachers['Male_CB'] + all_teachers['Female_CB']
    show_gender_percentages("Career breaks by gender", all_teachers, "Male_CB", "Female_CB", "All_CB")
    '''
    # calculate percentage of male teachers that have taken career breaks each year
    all_teachers['male_percent'] = all_teachers['Male_cb']/all_teachers['All_tot'] * 100
    # calculate percentage of female teachers that have taken career breaks each year
    #percents = pd.DataFrame()
    all_teachers['female_percent'] = all_teachers['Female_cb'] / all_teachers['All_tot'] * 100

    percents = all_teachers.loc[:,['Year', 'male_percent', 'female_percent']]
    # flip to tall dataframe
    percents = percents.melt(id_vars=['Year'])
    print(percents)
    
    

    # show on a simple bar plot
    sns.catplot(kind='bar', data=percents, x='Year', y='value', hue="variable")
    # Show plot
    plt.show()

    print(all_teachers.head(10))
    '''

def show_principals(all_teachers):
    print(all_teachers.head(1))
    print('hurah')
    all_teachers["All_Prin"] = all_teachers['Male_Prin'] + all_teachers['Female_Prin']
    show_gender_percentages("Teachers by gender", all_teachers, "Male_All", "Female_All", "All" )
    show_gender_percentages("Principals by gender", all_teachers, "Male_Prin", "Female_Prin", "All_Prin")


def show_gender_percentages(title, totals, male_col, female_col, total_col):
    print(totals.head())
    # calculate 2 extra cols for percentage of male and female
    p1 = 'Male'
    p2 = 'Female'
    totals[p1] = totals[male_col]/totals[total_col] * 100
    totals[p2] = totals[female_col] / totals[total_col] * 100

    # create new dataframe with just the Year and percentages cols
    percents = totals.loc[:,['Year', p1, p2]]
    # melt to tall dataframe
    percents = percents.melt(id_vars=['Year'], var_name='Gender', value_name='percent')

    # show on a simple grouped bar plot
    p = sns.catplot(kind='bar', data=percents, x='Year', y='percent', hue="Gender")
    p.set_axis_labels("School Year", "Percentages")
    plt.title(title)

    # show same scale for all
    plt.yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], ["", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"])
    # Show plot
    plt.show()



def show_teacher_population(totals):

    p = sns.lineplot(data=totals, x='Year2', y='All')
    # plt.xticks(rotation=0)
    # plt.xticks([2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020])

    p.set(xlabel='School Year', ylabel='Number of teachers')
    plt.title("Teacher Population overall")
    plt.show()
