#!/usr/bin/env python3

import numpy as np

cases_total_csv = np.genfromtxt('/home/nuke/git/covid-19-data/us_covid-19_cases_total.csv', dtype='int32')
deaths_total_csv = np.genfromtxt('/home/nuke/git/covid-19-data/us_covid-19_deaths_total.csv', dtype='int32')

cases_total = np.array(cases_total_csv)
cases_diff = np.diff(cases_total)
cases_daily = np.insert(cases_diff, 0, 0)

deaths_total = np.array(deaths_total_csv)
deaths_diff = np.diff(deaths_total)
deaths_daily = np.insert(deaths_diff, 0, 0)

np.savetxt('us_covid-19_deaths_daily.csv', deaths_daily, fmt='%d')
np.savetxt('us_covid-19_cases_daily.csv', cases_daily, fmt='%d')
