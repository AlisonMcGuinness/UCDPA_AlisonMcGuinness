# This is a sample Python script.
from import_teachers import get_teacher_data, tidy_teacher_data
from import_pupils import get_pupil_data, clean_pupil_data
from show_teachers import show_career_breaks, show_principals, show_teacher_population
from show_pupils import show_pupils
from pupil_teacher import show_pupil_teachers, merge_pupil_teachers


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Extract Teacher Statistics Data
raw_careers, raw_job_sharing, raw_totals = get_teacher_data()

# Tidy Data
careers, job_sharing, totals = tidy_teacher_data(raw_careers, raw_job_sharing, raw_totals)

# Graph teachers
#show_career_breaks(careers, totals)
##show_principals(totals)
#show_teacher_population(totals)

# Get Pupil data
pupils = get_pupil_data()
pupils = clean_pupil_data(pupils)
#show_pupils(pupils)

# Show pupils and teacher data together
pt = merge_pupil_teachers(pupils, totals)
show_pupil_teachers(pt)
