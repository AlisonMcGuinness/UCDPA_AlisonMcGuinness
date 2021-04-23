"""
main.py
created 17/04/21
UCD Certificate in Introductory Data Science.

This is main control code, run main.py to see all results.
"""
import numpy as np
from import_teachers import get_teacher_data, clean_teacher_data
from import_pupils import get_pupil_data, clean_pupil_data
from import_schools import get_schools_data

from show_teachers import show_career_breaks, show_principals, show_gender_pie, show_teacher_population
from show_pupils import show_pupils
from pupil_teacher import show_pupil_teachers, merge_pupil_teachers
from show_class_size import show_class_sizes


def do_teachers():
    # Extract Teacher Statistics Data
    raw_careers, raw_job_sharing, raw_totals = get_teacher_data()

    # Tidy Data
    careers, job_sharing, totals = clean_teacher_data(raw_careers, raw_job_sharing, raw_totals)

    # Graph teacher information
    show_career_breaks(careers, totals)
    show_principals(totals)
    show_teacher_population(totals)
    show_gender_pie(totals)

    return totals

def do_pupils(teachers):
    # Get Pupil data
    pupils = get_pupil_data()
    pupils = clean_pupil_data(pupils)
    show_pupils(pupils)

    # Show pupils and teacher data together
    pt = merge_pupil_teachers(pupils, teachers)
    show_pupil_teachers(pt)

# example of using iterrows to process a dataframe
def iter_teachers(teachers):
    print('Iterate through a dataframe')
    total = 0
    for row_lable, row_data in teachers.iterrows():
        print(row_lable, row_data)
        total += row_data["Female_All"]
    print("Total female teachers using iterrows is %d" % total)

# example of using numpy to sum a column
def numpy_teachers(teachers):
    print('Get total using numpy method')
    numpy_data = teachers["Female_All"]
    print(type(numpy_data))
    print("Total female teacher using numpy is %d" % np.sum(numpy_data))


def do_schools():
    schools, school_classes = get_schools_data()
    show_class_sizes(school_classes)
    return schools

# this runs everything!
teachers = do_teachers()
iter_teachers(teachers)
numpy_teachers(teachers)
do_pupils(teachers)
schools = do_schools()

