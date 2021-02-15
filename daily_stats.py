#!/usr/bin/env python3

import numpy as np
import os
import datetime

def prepend_line(file_name, line):
    dummy_file = file_name + '.bak'
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        write_obj.write(line + '\n')
        for line in read_obj:
            write_obj.write(line)
    os.remove(file_name)
    os.rename(dummy_file, file_name)

cases_daily_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_cases_daily.csv', dtype='int32')
deaths_daily_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_deaths_daily.csv', dtype='int32')

cases_array = np.array(cases_daily_csv)
cases_length = len(cases_array)
cases_today = cases_array[cases_length - 1]

deaths_array = np.array(deaths_daily_csv)
deaths_length = len(deaths_array)
deaths_today = deaths_array[deaths_length - 1]

today = datetime.datetime.today().strftime('%m-%d-%Y')

line = '# US COVID-19 Data\n## ' + str(today) + ' Statistics\n#### <pre> +--------------+---------------+ </pre>\n#### <pre> | Cases Today  |  Deaths Today | </pre>\n#### <pre> | ' + str(cases_today) + '        | ' + " " + str(deaths_today) + '         | </pre>\n#### <pre> +--------------+---------------+ </pre>'

prepend_line("README.md", line)
