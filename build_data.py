#!/usr/bin/env python3

import requests
import pandas as pd
import io
import numpy as np

def build_data():
    # Fetch data
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    download = requests.get(url).content
    df = pd.read_csv(io.StringIO(download.decode('utf-8')))
    df.to_csv("us.csv", index=False)

    # Extract each column individually
    dates = pd.read_csv('/home/nuke/git/covid-19-data/us.csv', usecols=['date'])
    cases_total = pd.read_csv('/home/nuke/git/covid-19-data/us.csv', usecols=['cases'])
    deaths_total = pd.read_csv('/home/nuke/git/covid-19-data/us.csv', usecols=['deaths'])

    # Create csv's for extracted columns
    dates.to_csv("/home/nuke/git/covid-19-data/data/us_covid-19_dates.csv", header=False, index=False)
    cases_total.to_csv("/home/nuke/git/covid-19-data/data/us_covid-19_cases_total.csv", header=False, index=False)
    deaths_total.to_csv("/home/nuke/git/covid-19-data/data/us_covid-19_deaths_total.csv", header=False, index=False)

    # csv files needed to build arrays
    cases_total_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_cases_total.csv', dtype='int32')
    deaths_total_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_deaths_total.csv', dtype='int32')

    # Calculate daily cases
    cases_total = np.array(cases_total_csv)
    cases_diff = np.diff(cases_total)
    cases_daily = np.insert(cases_diff, 0, 1)

    # Calculate daily deaths
    deaths_total = np.array(deaths_total_csv)
    deaths_diff = np.diff(deaths_total)
    deaths_daily = np.insert(deaths_diff, 0, 0)

    # Create csv's for daily cases and deaths
    np.savetxt('/home/nuke/git/covid-19-data/data/us_covid-19_deaths_daily.csv', deaths_daily, fmt='%d')
    np.savetxt('/home/nuke/git/covid-19-data/data/us_covid-19_cases_daily.csv', cases_daily, fmt='%d')

    # Create csv for daily data
    df = pd.read_csv('/home/nuke/git/covid-19-data/data/us_covid-19_dates.csv', header=0, names=['date'])
    cases_daily = pd.read_csv('/home/nuke/git/covid-19-data/data/us_covid-19_cases_daily.csv', header=None, dtype=str)      
    deaths_daily = pd.read_csv('/home/nuke/git/covid-19-data/data/us_covid-19_deaths_daily.csv', header=None, dtype=str)
    df["daily cases"] = cases_daily
    df["daily deaths"] = deaths_daily
    df.to_csv("/home/nuke/git/covid-19-data/data/us_covid-19_daily.csv", index=False)

    # Create csv for total data                                                                                                 
    cases_total = pd.read_csv('/home/nuke/git/covid-19-data/data/us_covid-19_cases_daily.csv', header=None, dtype=str)      
    deaths_total = pd.read_csv('/home/nuke/git/covid-19-data/data/us_covid-19_deaths_daily.csv', header=None, dtype=str)
    df["toal cases"] = cases_total
    df["total deaths"] = deaths_total
    df.to_csv("/home/nuke/git/covid-19-data/data/us_covid-19_total.csv", index=False)

    # Create csv for all aggregated data
    df = pd.read_csv('/home/nuke/git/covid-19-data/data/us_covid-19_data.csv', header=0, names=['date', 'total cases', 'total deaths'])
    df["daily cases"] = cases_daily
    df["daily deaths"] = deaths_daily
    df.to_csv("/home/nuke/git/covid-19-data/data/us_covid-19_data.csv", index=False)
