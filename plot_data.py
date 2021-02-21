#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def plot_data():
    # csv files needed for arrays
    dates_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_dates.csv', dtype='datetime64')
    total_cases_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_total_cases.csv', dtype='int32')
    total_deaths_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_total_deaths.csv', dtype='int32')
    new_cases_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_new_cases.csv', dtype='int32')
    new_deaths_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_new_deaths.csv', dtype='int32')

    # X axis for all plots
    x = np.array(dates_csv)

    # Plot Total Cases
    y = np.array((total_cases_csv) / 1000000)

    plt.figure('US Total COVID-19 Cases', figsize=(15, 8))
    plt.title("US Total COVID-19 Cases")
    plt.ylabel("Cases (in millions)")
    plt.grid(True, ls = "-.")
    plt.yticks(np.arange(min(y), max(y) + 10))
    plt.plot(x, y, color = "b")
    plt.savefig("/home/nuke/git/covid-19-data/plots/US_Total_COVID-19_Cases.png")
    #plt.show()

    # Plot Total Deaths
    y = np.array((total_deaths_csv) / 1000)

    plt.figure('US Total COVID-19 Deaths', figsize=(15, 8))
    plt.title("US Total COVID-19 Deaths")
    plt.ylabel("Deaths (in thousands)")
    plt.grid(True, ls = "-.")
    plt.yticks(np.arange(min(y), max(y) + 100, 50))
    plt.plot(x, y, color = "b")
    plt.savefig("/home/nuke/git/covid-19-data/plots/US_Total_COVID-19_Deaths.png")
    #plt.show()

    # Plot New Cases
    y = np.array((new_cases_csv) / 1000)

    plt.figure('US New COVID-19 Cases', figsize=(15, 8))
    plt.title("US New COVID-19 Cases")
    plt.ylabel("Cases (in thousands)")
    plt.grid(True, ls = "-.")
    plt.yticks(np.arange(min(y), max(y) + 100, 50))
    plt.plot(x, y, color = "b")
    plt.savefig("/home/nuke/git/covid-19-data/plots/US_New_COVID-19_Cases.png")
    #plt.show()

    # Plot New Deaths
    y = np.array(new_deaths_csv)

    plt.figure('US New COVID-19 Deaths', figsize=(15, 8))
    plt.title("US New COVID-19 Deaths")
    plt.ylabel("Deaths")
    plt.grid(True, ls = "-.")
    plt.yticks(np.arange(min(y), max(y) + 1000, 500))
    plt.plot(x, y, color = "b")
    plt.savefig("/home/nuke/git/covid-19-data/plots/US_New_COVID-19_Deaths.png")
    #plt.show()
