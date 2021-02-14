#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

dates_csv = np.genfromtxt('/home/nuke/git/covid-19/us_covid-19_dates.csv', dtype='datetime64')
deaths_daily_csv = np.genfromtxt('/home/nuke/git/covid-19/us_covid-19_deaths_daily.csv', dtype='int32')

x = np.array(dates_csv)
z = np.array(deaths_daily_csv)

plt.figure('US Daily COVID-19 Deaths', figsize=(15, 8))
plt.title("US Daily COVID-19 Deaths")
plt.ylabel("Deaths")
plt.grid(True, ls = "-.")
plt.yticks(np.arange(min(z), max(z) + 1000, 500))
plt.plot(x, z, color = "b")
plt.show()
