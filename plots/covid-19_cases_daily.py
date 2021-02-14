#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

dates_csv = np.genfromtxt('/home/nuke/git/covid-19-data/us_covid-19_dates.csv', dtype='datetime64')
cases_daily_csv = np.genfromtxt('/home/nuke/git/covid-19-data/us_covid-19_cases_daily.csv', dtype='int32')

x = np.array(dates_csv)
z = np.array((cases_daily_csv) / 1000)

plt.figure('US Daily COVID-19 Cases', figsize=(15, 8))
plt.title("US Daily COVID-19 Cases")
plt.ylabel("Cases (in thousands)")
plt.grid(True, ls = "-.")
plt.yticks(np.arange(min(z), max(z) + 100, 50))
plt.plot(x, z, color = "b")
plt.show()
