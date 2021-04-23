"""
show_class_size.py
created: 20/04/21

show distribution of class sizes for all primary schools

"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def show_class_sizes(all_classes):
    s = sns.relplot(x='year', y='value', ci=None, data=all_classes, kind='line', hue="Province")
    s.set(xlabel="School year", ylabel="Average students per class")
    title = "Average class size by province"
    plt.title(title)
    plt.show()
    plt.figure().savefig("images\\%s" % title)
