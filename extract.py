#!/usr/bin/env python3

import pandas as pd

dates = pd.read_csv('/home/nuke/git/covid-19-data/us.csv', usecols=['date'])
cases_total = pd.read_csv('/home/nuke/git/covid-19-data/us.csv', usecols=['cases'])
deaths_total = pd.read_csv('/home/nuke/git/covid-19-data/us.csv', usecols=['deaths'])

dates.to_csv("us_covid-19_dates.csv", header=False, index=False)
cases_total.to_csv("us_covid-19_cases_total.csv", header=False, index=False)
deaths_total.to_csv("us_covid-19_deaths_total.csv", header=False, index=False)
