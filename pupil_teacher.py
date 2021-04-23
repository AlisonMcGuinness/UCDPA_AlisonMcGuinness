"""
pupil_teacher.py
created: 18/04/21

methods for merging pupil/teacher together and showing on graph
"""
import matplotlib.pyplot as plt
import seaborn as sns


def merge_pupil_teachers(pupils, teachers):
    # group all pupils by year so one row per year
    yearly = pupils.groupby(["Year"]).agg({"VALUE": "sum"})
    # merge with the teachers so each row has year, total students and total teachers
    pt = yearly.merge(teachers, on="Year")
    return pt


def show_pupil_teachers(pt):
    # print(pt.head(30))
    # print(pt.shape)
    # Make a new column with the student/teacher ratio for each yer
    pt["ratio"] = pt["VALUE"] / pt["All"]

    p = sns.lineplot(data=pt, x="Year", y="ratio", marker="o")
    plt.xticks([2014, 2015, 2016, 2017])
    p.set(xlabel="School Year", ylabel="Students per Teacher")
    title = "Primary School Student-Teacher ratio by year"
    plt.title(title)
    plt.show()
    plt.savefig("images\\%s" % title)
