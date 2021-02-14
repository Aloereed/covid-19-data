#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

cases_dates_csv = np.genfromtxt('/home/nuke/git/covid-19/us_covid-19_cases_dates.csv', dtype='datetime64')
cases_total_csv = np.genfromtxt('/home/nuke/git/covid-19/us_covid-19_cases_total.csv', dtype='int32')

x = np.array(cases_dates_csv)
y = np.array((cases_total_csv) / 1000000)

plt.figure('US Total COVID-19 Cases', figsize=(15, 8))
plt.title("US Total COVID-19 Cases")
plt.ylabel("Cases (in millions)")
plt.grid(True, ls = "-.")
plt.yticks(np.arange(min(y), max(y) + 10))
plt.plot(x, y, color = "b")
plt.show()
