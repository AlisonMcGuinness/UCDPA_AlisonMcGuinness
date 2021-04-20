"""
show_class_size.py
created: 20/04/21

show distribution of class sizes for all primary schools

"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def test():

    headers = ["type", "value"]
    data= [["Leinster", 25],["Leinster", 32],["Leinster",33],["Leinster", 26],["Leinster", 27],
           ["Munster", 21],["Munster", 25],["Munster", 18],["Munster", 21],["Munster", 23]]
    all = pd.DataFrame(data, columns=headers)
    print(all.head())
    show_class_sizes(all)

def show_class_sizes(all_classes):
    sns.distplot(all_classes['value'],
             kde=True, # disable the KDE line, this just makes a hist plot
             bins=20,  # set number of bins
             hist=True,
             rug=False,  # shows values underneath?? shows how the values are distributed?
             kde_kws={'shade': True})  # can pass in cus
    plt.show()

    sns.histplot(data = all_classes, x ="value", hue = "type", alpha=0.2)
    plt.show()

    # gropu by(lvel=0) means group by the 0 level which is the index?
    avg_class = all_classes.groupby('type').agg({'value':'mean'})

    # Bar plot of avg_inv_by_month
    avg_class.plot(kind="bar")
    plt.show()