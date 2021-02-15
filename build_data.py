#!/usr/bin/env python3

import requests
import pandas as pd
import io
import numpy as np
from plot_data import*
from daily_stats import*

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

# Calculate the difference of total values to determine daily deltas

# csv files
cases_total_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_cases_total.csv', dtype='int32')
deaths_total_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_deaths_total.csv', dtype='int32')
    
# Calculate the difference

# Cases
cases_total = np.array(cases_total_csv)
cases_diff = np.diff(cases_total)
cases_daily = np.insert(cases_diff, 0, 1)

# Deaths
deaths_total = np.array(deaths_total_csv)
deaths_diff = np.diff(deaths_total)
deaths_daily = np.insert(deaths_diff, 0, 0)

# Create csv
np.savetxt('/home/nuke/git/covid-19-data/data/us_covid-19_deaths_daily.csv', deaths_daily, fmt='%d')
np.savetxt('/home/nuke/git/covid-19-data/data/us_covid-19_cases_daily.csv', cases_daily, fmt='%d')

# Aggregate all new data to one file

# csv files
df = pd.read_csv('/home/nuke/git/covid-19-data/us.csv', header=0, names=['date', 'total cases', 'total deaths'])
cases_daily = pd.read_csv('/home/nuke/git/covid-19-data/data/us_covid-19_cases_daily.csv', header=None, dtype=str)
deaths_daily = pd.read_csv('/home/nuke/git/covid-19-data/data/us_covid-19_deaths_daily.csv', header=None, dtype=str)

# Create csv
df["daily cases"] = cases_daily
df["daily deaths"] = deaths_daily
df.to_csv("us_covid-19_data.csv", index=False)

# Plot all data to png files
plot_cases_total()
plot_deaths_total()
plot_cases_daily()
plot_deaths_daily()

# Build daily status and write to 'daily_stats.md'
create_daily_stats()
