# This is a sample Python script.
from webscrape import do_webscrape, tidy_teacher_data
from visualise import show_career_breaks, show_principals


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Extract Teacher Statistics Data
raw_careers, raw_jobsharing, raw_totals = do_webscrape()

# Tidy Data
careers, job_sharing, totals = tidy_teacher_data(raw_careers, raw_jobsharing, raw_totals)

# Graph teachers
show_career_breaks(careers, totals)
show_principals(totals)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
