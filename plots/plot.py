#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

# Plot Total Cases
def plot_cases_total():
    dates_csv = np.genfromtxt('/home/nuke/git/covid-19-data/us_covid-19_dates.csv', dtype='datetime64')
    cases_total_csv = np.genfromtxt('/home/nuke/git/covid-19-data/us_covid-19_cases_total.csv', dtype='int32')

    x = np.array(dates_csv)
    y = np.array((cases_total_csv) / 1000000)

    plt.figure('US Total COVID-19 Cases', figsize=(15, 8))
    plt.title("US Total COVID-19 Cases")
    plt.ylabel("Cases (in millions)")
    plt.grid(True, ls = "-.")
    plt.yticks(np.arange(min(y), max(y) + 10))
    plt.plot(x, y, color = "b")
    plt.show()

# Plot Total Deaths
def plot_deaths_total():
    dates_csv = np.genfromtxt('/home/nuke/git/covid-19-data/us_covid-19_dates.csv', dtype='datetime64')
    deaths_total_csv = np.genfromtxt('/home/nuke/git/covid-19-data/us_covid-19_deaths_total.csv', dtype='int32')

    x = np.array(dates_csv)
    y = np.array((deaths_total_csv) / 1000)

    plt.figure('US Total COVID-19 Deaths', figsize=(15, 8))
    plt.title("US Total COVID-19 Deaths")
    plt.ylabel("Deaths (in thousands)")
    plt.grid(True, ls = "-.")
    plt.yticks(np.arange(min(y), max(y) + 100, 50))
    plt.plot(x, y, color = "b")
    plt.show()

# Plot Daily Cases
def plot_cases_daily():
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

# Plot Daily Deaths
def plot_deaths_daily():
    dates_csv = np.genfromtxt('/home/nuke/git/covid-19-data/us_covid-19_dates.csv', dtype='datetime64')
    deaths_daily_csv = np.genfromtxt('/home/nuke/git/covid-19-data/us_covid-19_deaths_daily.csv', dtype='int32')

    x = np.array(dates_csv)
    z = np.array(deaths_daily_csv)

    plt.figure('US Daily COVID-19 Deaths', figsize=(15, 8))
    plt.title("US Daily COVID-19 Deaths")
    plt.ylabel("Deaths")
    plt.grid(True, ls = "-.")
    plt.yticks(np.arange(min(z), max(z) + 1000, 500))
    plt.plot(x, z, color = "b")
    plt.show()

plot_cases_total()
plot_deaths_total()
plot_cases_daily()
plot_deaths_daily()
