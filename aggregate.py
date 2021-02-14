#!/usr/bin/env python3

import pandas as pd

# .csv files
df = pd.read_csv('/home/nuke/git/covid-19-data/us.csv')
cases_daily = pd.read_csv('/home/nuke/git/covid-19-data/us_covid-19_cases_daily.csv', header=None, dtype=str)
deaths_daily = pd.read_csv('/home/nuke/git/covid-19-data/us_covid-19_deaths_daily.csv', header=None, dtype=str)

# Aggregate data
df["daily cases"] = cases_daily
df["daily deaths"] = deaths_daily
df.to_csv("us_covid-19_data.csv", index=False)
