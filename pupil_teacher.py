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
    pt = yearly.merge(teachers, on="Year")
    return pt


def show_pupil_teachers(pt):
    print(pt.head(30))
    print(pt.shape)
    # Get the student teacher ratio for each yer
    pt["ratio"] = pt["VALUE"] / pt["All"]

    p = sns.lineplot(data=pt, x="Year", y="ratio", marker="o")

    p.set(xlabel="School Year", ylabel="Students per Teacher")
    plt.title("Student Teacher ratio by year")
    plt.show()
