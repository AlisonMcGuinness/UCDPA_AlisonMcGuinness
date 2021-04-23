"""
show_pupils.py
created 18/04/21

methods to visualise primary pupil data

"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# class groupings to simplify graph
cls_JS = "Junior/Senior Infants"
cls_12 = "1st/2nd Class"
cls_34 = "3rd/4th Class"
cls_56 = "5th/6th Class"


# create graphs from pupils dataframe
def show_pupils(pupils):
    sns.set_style("whitegrid")
    # Group data to get sum of pupils by year and class
    class_sum = pupils.groupby(['Year', 'School Programme']).agg({'VALUE': 'sum'})
    class_sum = class_sum.reset_index()

    # filter to just show the classes that we are interested in
    include = ["Junior infants", "Senior infants", "1st class", "2nd class", "3rd class", "4th class", "5th class",
               "6th class"]
    included_data = class_sum[class_sum["School Programme"].isin(include)]

    included_data.rename(columns={"School Programme": "School Class"}, inplace=True)
    """
    First try with a line on the graph for each class was too hard to read the graph (there are 8 classes)
    line_plot = sns.lineplot(data=included_data, x='Year', y='VALUE', hue="School Class", hue_order=include)
    plt.xticks(rotation=0)
    plt.xticks([2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020])
    line_plot.set(xlabel='School Year', ylabel='Number of students')
    plt.title("Student Population by class")
    plt.show()    
    """
    # 8 lines is too many on the graph so try grouping classes together
    included_data["Class Group"] = included_data["School Class"].apply(set_class_group)
    line_plot = sns.lineplot(data=included_data, x='Year', y='VALUE', ci=None, \
                hue="Class Group", marker="o", hue_order=[cls_JS, cls_12, cls_34, cls_56])

    plt.xticks(rotation=0)
    plt.xticks([2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020])

    line_plot.set(xlabel='School Year', ylabel='Number of students')
    title = "Primary School Student Population by classes"
    plt.title(title)
    plt.show()
    plt.figure().savefig("images\\%s" % title)

    print('group by YEAR')
    # Now show another graph with the overall student population totals for each year
    yearly = pupils.groupby(['Year']).agg({'VALUE': 'sum'})
    print(yearly.head())

    p = sns.lineplot(data=yearly, x='Year', y='VALUE', marker="o")
    plt.xticks(rotation=0)
    plt.xticks([2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020])

    p.set(xlabel='School Year', ylabel='Number of students')
    title = "Primary School Student Population overall"
    plt.title(title)
    plt.savefig("images\\%s" % title)
    plt.show()


# group classes together in pairs to reduce lines on graph
def set_class_group(class_name):
    if class_name.lower() in ['junior infants', 'senior infants']:
        return cls_JS
    elif class_name.lower() in ['1st class', '2nd class']:
        return cls_12
    elif class_name.lower() in ['3rd class', '4th class']:
        return cls_34
    elif class_name.lower() in ['5th class', '6th class']:
        return cls_56
    else:
        print("NO CLASS FOUND")
    return ""
