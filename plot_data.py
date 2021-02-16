#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def plot_data():
# Plot Total Cases
    dates_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_dates.csv', dtype='datetime64')
    cases_total_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_cases_total.csv', dtype='int32')

    x = np.array(dates_csv)
    y = np.array((cases_total_csv) / 1000000)

    plt.figure('US Total COVID-19 Cases', figsize=(15, 8))
    plt.title("US Total COVID-19 Cases")
    plt.ylabel("Cases (in millions)")
    plt.grid(True, ls = "-.")
    plt.yticks(np.arange(min(y), max(y) + 10))
    plt.plot(x, y, color = "b")
    plt.savefig("/home/nuke/git/covid-19-data/plots/US_Total_COVID-19_Cases.png")
    plt.show()

# Plot Total Deaths
    dates_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_dates.csv', dtype='datetime64')
    deaths_total_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_deaths_total.csv', dtype='int32')

    x = np.array(dates_csv)
    y = np.array((deaths_total_csv) / 1000)

    plt.figure('US Total COVID-19 Deaths', figsize=(15, 8))
    plt.title("US Total COVID-19 Deaths")
    plt.ylabel("Deaths (in thousands)")
    plt.grid(True, ls = "-.")
    plt.yticks(np.arange(min(y), max(y) + 100, 50))
    plt.plot(x, y, color = "b")
    plt.savefig("/home/nuke/git/covid-19-data/plots/US_Total_COVID-19_Deaths.png")
    plt.show()

# Plot Daily Cases
    dates_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_dates.csv', dtype='datetime64')
    cases_daily_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_cases_daily.csv', dtype='int32')

    x = np.array(dates_csv)
    z = np.array((cases_daily_csv) / 1000)

    plt.figure('US Daily COVID-19 Cases', figsize=(15, 8))
    plt.title("US Daily COVID-19 Cases")
    plt.ylabel("Cases (in thousands)")
    plt.grid(True, ls = "-.")
    plt.yticks(np.arange(min(z), max(z) + 100, 50))
    plt.plot(x, z, color = "b")
    plt.savefig("/home/nuke/git/covid-19-data/plots/US_Daily_COVID-19_Cases.png")
    plt.show()

# Plot Daily Deaths
    dates_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_dates.csv', dtype='datetime64')
    deaths_daily_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_deaths_daily.csv', dtype='int32')

    x = np.array(dates_csv)
    z = np.array(deaths_daily_csv)

    plt.figure('US Daily COVID-19 Deaths', figsize=(15, 8))
    plt.title("US Daily COVID-19 Deaths")
    plt.ylabel("Deaths")
    plt.grid(True, ls = "-.")
    plt.yticks(np.arange(min(z), max(z) + 1000, 500))
    plt.plot(x, z, color = "b")
    plt.savefig("/home/nuke/git/covid-19-data/plots/US_Daily_COVID-19_Deaths.png")
    plt.show()
