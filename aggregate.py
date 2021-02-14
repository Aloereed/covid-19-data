#!/usr/bin/env python3

from fetch import fetch_data
import pandas as pd

# Fetch Data
fetch_data()

# .csv files
df = pd.read_csv('/home/nuke/git/covid-19-data/us.csv')
cases_daily = pd.read_csv('/home/nuke/git/covid-19-data/us_covid-19_cases_daily.csv', dtype=str)
deaths_daily = pd.read_csv('/home/nuke/git/covid-19-data/us_covid-19_deaths_daily.csv', dtype=str)

# Aggregate data
df["daily cases"] = cases_daily
df["daily deaths"] = deaths_daily
df.to_csv("us_covid-19_data.csv", index=False)
