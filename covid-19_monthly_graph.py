#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

dates_csv = np.genfromtxt('/home/nuke/git/covid-19/us_covid-19_dates.csv', dtype='datetime64')
total_deaths_csv = np.genfromtxt('/home/nuke/git/covid-19/us_covid-19_total_deaths.csv', dtype='int32')
daily_deaths_csv = np.genfromtxt('/home/nuke/git/covid-19/us_covid-19_daily_deaths.csv', dtype='int32')

x = np.array(dates_csv)
y = np.array(total_deaths_csv)
z = np.array(daily_deaths_csv)

plt.figure(figsize=(15, 8))
plt.title("COVID-19 Monthly Deaths")
plt.xlabel("Date")
plt.ylabel("Deaths")
plt.grid(True, ls = "-.")
plt.yticks(np.arange(min(z), max(z)+500, 250))
plt.plot(x, z, color = "b")
plt.show()
