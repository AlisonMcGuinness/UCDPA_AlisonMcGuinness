"""
show_pupils.py
created 18/04/21

methods to visualise primary pupil data

"""
import matplotlib.pyplot as plt
import seaborn as sns

# create graphs from pupils dataframe
def show_pupils(pupils):
    # Group data to get sum of pupils by year and class
    class_sum = pupils.groupby(['Year', 'School Programme']).agg({'VALUE': 'sum'})
    class_sum = class_sum.reset_index()

    # filter to just show the classes that we are interested in
    include = ["Junior infants", "Senior infants", "1st class", "2nd class", "3rd class", "4th class", "5th class",
               "6th class"]
    included_data = class_sum[class_sum["School Programme"].isin(include)]
    # df.rename(columns ={"":"Test","header2":"test2"}, inplace=True)
    included_data.rename(columns={"School Programme":"School Class"}, inplace=True)

    line_plot = sns.lineplot(data=included_data, x='Year', y='VALUE', hue="School Class")
    plt.xticks(rotation=0)
    plt.xticks([2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020])
    # p.set_axis_labels("School Year", "Number of students")
    line_plot.set(xlabel='School Year', ylabel='Number of students')
    plt.title("Student Population by class")
    plt.show()

    print('group by YEAR')
    yearly = pupils.groupby(['Year']).agg({'VALUE': 'sum'})
    print(yearly.info())

    p = sns.lineplot(data=yearly, x='Year', y='VALUE')
    plt.xticks(rotation=0)
    plt.xticks([2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020])
    # p.set_axis_labels("School Year", "Number of students")
    p.set(xlabel='School Year', ylabel='Number of students')
    plt.title("Student Population overall")
    plt.show()

