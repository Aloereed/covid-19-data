#!/usr/bin/env python3

from build_data import date, total_cases, total_deaths, new_cases, new_deaths
import numpy as np
import matplotlib.pyplot as plt

# x axis for all plots
x = np.array(date, dtype='datetime64')

# Plot Total Cases
y = total_cases / 1000000
plt.figure('US Total COVID-19 Cases', figsize=(15, 8))
plt.title('US Total COVID-19 Cases')
plt.ylabel('Cases (in millions)')
plt.grid(True, ls='-.')
plt.yticks(np.arange(min(y), max(y) + 10))
plt.plot(x, y, color='b')
plt.savefig('plots/US_Total_COVID-19_Cases.png')
plt.show()

# Plot Total Deaths
y = total_deaths / 1000
plt.figure('US Total COVID-19 Deaths', figsize=(15, 8))
plt.title('US Total COVID-19 Deaths')
plt.ylabel('Deaths (in thousands)')
plt.grid(True, ls='-.')
plt.yticks(np.arange(min(y), max(y) + 100, 50))
plt.plot(x, y, color='b')
plt.savefig('plots/US_Total_COVID-19_Deaths.png')
plt.show()

# Plot New Cases
y = new_cases / 1000
plt.figure('US New COVID-19 Cases', figsize=(15, 8))
plt.title('US New COVID-19 Cases')
plt.ylabel('Cases (in thousands)')
plt.grid(True, ls='-.')
plt.yticks(np.arange(min(y), max(y) + 100, 50))
plt.plot(x, y, color='b')
plt.savefig('plots/US_New_COVID-19_Cases.png')
plt.show()

# Plot New Deaths
y = new_deaths
plt.figure('US New COVID-19 Deaths', figsize=(15, 8))
plt.title('US New COVID-19 Deaths')
plt.ylabel('Deaths')
plt.grid(True, ls='-.')
plt.yticks(np.arange(min(y), max(y) + 1000, 500))
plt.plot(x, y, color='b')
plt.savefig('plots/US_New_COVID-19_Deaths.png')
plt.show()
