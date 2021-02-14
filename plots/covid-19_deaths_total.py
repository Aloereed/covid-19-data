#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

deaths_dates_csv = np.genfromtxt('/home/nuke/git/covid-19/us_covid-19_deaths_dates.csv', dtype='datetime64')
deaths_total_csv = np.genfromtxt('/home/nuke/git/covid-19/us_covid-19_deaths_total.csv', dtype='int32')

x = np.array(deaths_dates_csv)
y = np.array((deaths_total_csv) / 1000)

plt.figure('US Total COVID-19 Deaths', figsize=(15, 8))
plt.title("US Total COVID-19 Deaths")
plt.ylabel("Deaths (in thousands)")
plt.grid(True, ls = "-.")
plt.yticks(np.arange(min(y), max(y) + 100, 50))
plt.plot(x, y, color = "b")
plt.show()
